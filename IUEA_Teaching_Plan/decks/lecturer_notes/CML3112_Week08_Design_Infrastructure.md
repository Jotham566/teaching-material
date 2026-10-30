# CML3112 Week 8

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: A first prediction model

Civil Engineering and Architecture

Tuesday 27 October 2026
Tuesday 11:00–14:00, Room 106

**Spoken script**

Welcome to Week 8. For seven weeks we have loaded, cleaned and charted data with Python and pandas.

Today we use that data to predict a number. We build three simple prediction models for cooling load, and we measure how far each one misses, in kW.

## Slide 2: Today’s learning

WHAT WE WILL DO
Predict cooling load from load and ambient temperature in three ways: the average, a straight line and a decision tree. Learn the words that go with them: feature, target, training, error and loss.

HOW YOU WILL SHOW IT
You can say in plain words what each method learned and read its error in kW. You can explain why some rows stay hidden while a model learns.

**Spoken script**

Today we build our first prediction models. We will predict cooling load from two inputs, using three methods. The first is the plain average. The second is a straight line. The third is a decision tree. Along the way we will name every idea we use, so that the words feature, target, training, error and loss all have a clear meaning by the end of the session. By the end you will be able to say what each method learned and read its error in kW.

## Slide 3: Today’s model is supervised regression

Supervised learning learns from examples that come with answers. Regression predicts a number.

**Spoken script**

Machine learning is a large field, so let us place today on a map. In supervised learning, every training example comes with its answer. Here an example is a past load reading together with the cooling load that was recorded. The model studies many of those pairs. When the answer is a number, the job is called regression. That is today. When the answer is a category, such as fault or no fault, the job is called classification, and that is next week. In unsupervised learning there are no answers, and the computer looks for groups by itself. We meet that in Semester 2. It includes grouping similar rows, called clustering, and squeezing many columns into fewer ones, called PCA. In reinforcement learning, a program learns by trial and reward. The Week 1 roadmap showed that this topic sits outside our course.

## Slide 4: Words for the whole field

**Spoken script**

Five words for the whole field. Machine learning means a computer finds the rule from examples. An algorithm is the recipe it follows, for example linear regression or a decision tree. A model is what you get after the recipe has studied your data. Same recipe, different data, different model. Training means showing the algorithm the examples so that it can set the numbers inside the model, and in scikit-learn that is one call, fit. A prediction is the model's answer for a row, and that is the call predict. Keep this table in mind. Every later slide uses these five words.

## Slide 5: Words for the data and the task

**Spoken script**

Now five words for the data. A feature is an input column, here the load percentage and the ambient temperature. The target is the column we want to predict, here cooling load. Regression is the job of predicting a number, so today is regression. Classification is predicting a category, and we meet it next week. Feature engineering means building a new input column from the ones you have, for example dividing the load by one hundred. We come to that in Week 11, and it is worth knowing the name today.

## Slide 6: The supplied file

Extract this week’s student ZIP. Upload engineering_data.csv into Colab using the Files panel, or keep them beside the notebook locally.

The examples below read this file. Run the cells in slide order. Keep the original CSV unchanged.

**Spoken script**

Every example today reads one file called engineering_data dot csv. A CSV file is a plain table saved as text, and it is the same kind of file we read in earlier weeks.

Extract this week's student ZIP folder on your computer. In Colab, Google's free online notebook, open the Files panel and upload engineering_data dot csv. If you work on your own machine, keep the file in the same folder as the notebook.

Uploading a notebook does not upload its data, so check that the file name is spelled exactly like this. Run the cells in the order the slides show them, because later cells use names created by earlier ones. Keep the original CSV unchanged, so you can always return to the starting point.

## Slide 7: Operations for the next example

01

Import and short names: import pandas as pd loads pandas and gives it the short name pd. pd.read_csv refers to a function in that library.

02

Reading a CSV: pd.read_csv("practice_filename.csv") reads the named file into a DataFrame: a table with labelled columns and row labels. The file must exist in the working folder.

03

Counting dimensions: equipment_data.shape gives (number of rows, number of columns). shape is a property, so it has no parentheses.

**Spoken script**

Three pandas ideas before the next example. Each one is a reminder from earlier weeks.

First, import pandas as pd loads the pandas library and gives it the short name pd. After that, pd dot read_csv means the read_csv function that lives inside pandas.

Second, pd dot read_csv with a file name in quotes reads that file into a DataFrame. A DataFrame is a table with named columns and a label for every row. The file must be in the working folder, or Python cannot find it.

Third, equipment_data dot shape tells us the size of the table as two numbers, the count of rows and then the count of columns. Shape is a property, a stored fact about the table, so we write it without parentheses.

## Slide 8: Operations for the next example

Column data types: equipment_data.dtypes reports each column’s stored type. int64 means integers, float64 means decimal numbers, and object often contains text. Numeric blanks commonly appear as NaN.

A preview of rows: equipment_data.head() returns the first five rows. It leaves the table unchanged. A preview is not the entire dataset.

**Spoken script**

Two more pandas tools for looking at a table.

dtypes reports the data type stored in each column. The type int64 means whole numbers. The type float64 means decimal numbers. The type object usually means text. A blank in a numeric column shows up as NaN, which stands for not a number and simply marks a missing value.

The head function shows the first five rows of the table. It is a quick preview and leaves the table as it was. Five rows are only a sample, so a preview tells us what the columns look like and says little about the whole dataset.

## Slide 9: Reading the code syntax

= assigns a value to a name; == compares values. Parentheses pass inputs or continue an expression across lines. print displays a value; len counts entries. int and float convert to integer and decimal numeric values.

**Spoken script**

Before we run the first example, a quick tour of the symbols in the code.

A single equals sign gives a value a name. So x equals five stores five under the name x. Two equals signs ask a question, are these two values the same, and the answer is True or False.

Parentheses hand inputs to a function. They can also let one long expression continue over several lines.

print shows a value on the screen. len counts how many entries something holds. int and float convert a value to a whole number or a decimal number.

With these in hand, the code on the next slides will read like short sentences.

## Slide 10: Loading the supplied observations

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

This first cell loads the data and takes a look at it, one line at a time.

The first line imports pandas under the short name pd. The second line reads engineering_data dot csv and stores the table under the name raw_data. This is the original table, and we never edit it, so we can always check our work against it.

The next three lines each print something. The head line shows the first five rows, so we can see the column names and what the values look like. The shape line prints the number of rows and then the number of columns. The dtypes line lists every column with its type, so we can spot a column that holds text where we expect numbers.

When we run the cell, each output matches what we just described.

## Slide 11: Some rows stay hidden while the model learns

Training rows teach. Validation rows compare models. Test rows are opened once, at the end.

**Spoken script**

Think about studying for an exam. The practice questions you study from play the part of the training rows. A mock exam that you sit to check your progress plays the part of the validation rows, and you may change how you study after it. The real exam plays the part of the test rows, and nobody sees its questions beforehand. If a model were scored on rows it had already studied, its score would look better than it deserves, in the same way that a student who has memorised the answers does well on the practice paper. In our data, equipment E1 to E4 train the model, E5 is the validation group, and E6 is the final test.

## Slide 12: Rows used for modelling

Keep the first occurrence of each record_id. Retain recorded targets and load_pct within 0–100. Then separate E1–E4 for training, E5 for validation and E6 for the final test_data.

Fill missing input values using training data only. Keep final-test targets out of model selection.

**Spoken script**

Before any model sees the data, we decide which rows are allowed in.

First we keep only the first occurrence of each record_id, so a record that was entered twice counts once. Then we keep rows where the target has a recorded value, and where load_pct lies between zero and one hundred, since a load outside that range is an error.

Then we split the remaining rows by equipment. Equipment E1 to E4 become the training rows, E5 becomes the validation rows, and E6 becomes the final test_data. Whole machines go to one group, so a machine never sits on both sides.

Missing input values are filled later, using training rows only. And the targets in the test group stay out of every choice we make.

## Slide 13: Operations for the next example

01

Reading chained operations: Read a chain from left to right. In equipment_data["target"].mean(), select the target Series first, then calculate its mean. Each step uses the previous step’s result.

02

A separate working table: equipment_data.copy() creates a working copy. Assigning columns on this copy preserves the source table, so you can compare before and after.

03

Finding recorded cells: notna() returns True where a value is present. Use it to retain observations with a recorded target before modelling.

**Spoken script**

Three operations we need for preparing the rows.

First, a chain of operations reads from left to right. In equipment_data, square brackets, quote target, then dot mean, we first pick the target column, which is a Series, one column of a table. Then we calculate its mean, the average. Each step works on the result of the step before.

Second, dot copy makes a separate working table. When we add or change columns on the copy, the original stays as it was, so we can compare before and after.

Third, notna gives True for every cell that has a value and False for every blank. We use it to keep only rows where the target was recorded.

## Slide 14: Operations for the next example

01

An inclusive range: series.between(0, 100) is True for values from 0 through 100, including both limits. The resulting mask helps select valid rows.

02

Selecting columns: equipment_data["column"] returns one labelled column, a Series. equipment_data[["a", "b"]] returns a DataFrame containing those named columns in that order.

03

Selecting rows with a mask: A column comparison produces one True or False per row. equipment_data[mask] keeps the True rows. & combines masks: both conditions must hold. Parenthesise each comparison.

**Spoken script**

Three more operations, all about picking out the rows and columns we want.

The between function takes two limits, for example zero and one hundred, and gives True for each value from the lower limit up to the upper limit. Both limits count as inside. The result is a mask, a column of True and False values, one for each row.

To select columns, one name in square brackets gives a single column, a Series. A list of names inside double square brackets gives a smaller table with those columns in that order.

To select rows, we compare a column with a value and get one True or False per row. Putting that mask in square brackets keeps the True rows. The ampersand joins two masks, and a row stays only when both are True. Put each comparison inside its own parentheses.

## Slide 15: Operations for the next example

Keeping the first observation: equipment_data.drop_duplicates("record_id") returns rows with the first occurrence of each ID, preserving their order. It does not overwrite the source unless you assign the result.

Membership in a group list: series.isin(["E1", "E2"]) returns True for entries matching either listed label. equipment_data[that_mask] keeps all observations belonging to those groups.

**Spoken script**

Two last operations before we prepare the rows.

drop_duplicates with the column name record_id keeps the first row for each ID and removes later repeats. The remaining rows stay in their original order. It gives us back a new table, so the source table changes only if we store the result under a name.

The isin function checks membership in a list. If we write isin with the labels E1 and E2 in a list, every row whose equipment ID is E1 or E2 gets True. Putting that mask in square brackets after the table keeps every observation from those machines.

## Slide 16: Prepare valid observations

First keep the first record ID.

Then ask two questions for each remaining row: is the target recorded, and is load between 0 and 100?

Only a row passing both checks stays.

Missing inputs are handled later using training data only.

**Spoken script**

We clean the table in two stages.

Stage one keeps the first row for each record ID, so repeated entries disappear.

Stage two asks two questions about every remaining row. Is the target recorded? Is the load between zero and one hundred percent? A row stays only when the answer to both is yes.

A row can still have a blank in one of its inputs. We leave that for later, because the fill value must come from the training rows alone.

## Slide 17: Preparing the supplied modelling rows: step 1

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

This cell applies those two stages. We read it line by line.

The first line removes repeated record IDs from raw_data and makes a copy, which we call modelling_data. The next line asks which rows have a recorded target and stores the True and False answers in target_is_recorded. The line after that asks which rows have a load between zero and one hundred. We combine the two answers with an ampersand, so rows_to_keep is True only when both checks pass.

The two print lines show the first five answers of each check. A False means that row will be dropped.

Then we keep only the True rows and copy them again. The last line prints two counts, the rows before cleaning and the rows after. The second count should be smaller or equal, and the gap tells us how many rows we removed.

## Slide 18: Choose groups before choosing rows

isin(list_of_labels) answers True when a row’s equipment ID appears in the list.

Here E1–E4 supply training rows, E5 validation rows and E6 test rows.

The groups stay separate so one equipment group cannot appear on both sides.

**Spoken script**

Now we choose which machines go into which group. The isin function answers True when a row's equipment ID appears in a list we give it.

Machines E1 to E4 supply the training rows, the examples the model learns from. Machine E5 supplies the validation rows, which we use to compare models. Machine E6 supplies the test rows, which we keep aside until the very end.

The groups stay separate. If one machine appeared on both sides, the model would be checked on data it had already seen, and the check would look better than it deserves.

## Slide 19: Preparing the supplied modelling rows: step 2

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

This cell builds three masks, one for each group. It prints nothing, because it only stores values for the next cell.

The first statement looks at the equipment_id column of modelling_data and uses isin with a list of E1, E2, E3 and E4. The result, is_training_equipment, is True for every row from those four machines.

The second statement does the same for the list that holds only E5, and gives is_validation_equipment. The third does it for E6 and gives is_test_equipment.

The code is spread over several lines only to fit the slide. Python reads the parentheses as one continuing statement.

## Slide 20: Preparing the supplied modelling rows: step 3

training_data: rows used to learn model settings; only these rows may determine imputation values.

validation_data: separate rows used to compare models without fitting on them.

**Spoken script**

Two names to keep in mind for the next cell.

training_data holds the rows the model learns from. Any value we fill in for a blank input is calculated from these rows only.

validation_data holds a separate set of rows. We use them to compare models, and we never fit anything on them. A model that has not seen these rows gives us an honest picture of how it behaves on new data.

## Slide 21: Preparing the supplied modelling rows: step 3

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

Here we cut the table into its three parts.

The first line keeps the rows picked by the training mask and copies them into training_data. The second does the same for the validation mask and gives validation_data. The third makes test_data, the rows we leave alone until the final evaluation.

Then feature_columns is a list of two column names, load_pct and ambient_c. These are the inputs we give the model, and we will call each input column a feature.

The print line shows three counts, the number of training rows, validation rows and test rows, in that order. The training count is the largest and no group is empty.

## Slide 22: A line through the points beats the average

Higher load goes with higher cooling load. The line follows the dots; the dashed average ignores load.

**Spoken script**

Here is our own data. Each dot is one observation. Load runs along the bottom, and the cooling load runs up the side. The dots rise from left to right, and across the 58 training rows the correlation between load and target is 0.94, which is strong. Correlation is a number between minus one and one that says how closely the dots follow a straight path. The dashed grey line is the training average. It predicts the same value for every row, whatever the load. The green line follows the dots, so it gives a different prediction for each load. The orange diamonds are the validation rows. The model never sees them while it learns, and we will check how far they sit from each prediction. The test rows are not drawn, because they stay sealed.

## Slide 23: Four misses, measured three ways

MAE  = mean of the absolute errors = 2.75 kW
MSE  = mean of the squared errors = 12.25 (kW squared)
RMSE = square root of the MSE = 3.5 kW
These four readings are invented to show the arithmetic.

**Spoken script**

Here are four invented readings, so that we can do the arithmetic by eye. For each reading, the error is the actual value minus the predicted value. Sometimes it is negative. The absolute error drops the sign. The squared error multiplies the error by itself, so a big miss counts a lot more than a small one. Now average. The mean of the absolute errors is the MAE, two point seven five. It is in the same unit as the target, so it reads as: on average we miss by two point seven five kW. The mean of the squared errors is the MSE, twelve point two five. Its unit is the target unit squared, which is awkward to read. Take its square root and we get the RMSE, three point five, back in kW. Because of the squaring, RMSE is bigger than MAE whenever some misses are larger than others. The squared version, the MSE, returns a little later as the loss that training tries to lower.

## Slide 24: Fitting a line to observations

The fitted line minimises the sum of squared vertical errors.

**Spoken script**

Fitting a line means choosing the straight line that follows the data best. To judge a line we look at each dot and measure the vertical gap between the dot and the line. That gap is the error for that observation.

We square each gap, which makes every error positive and makes big gaps count more. Then we add them up. Different lines give different totals. The fitted line is the one with the smallest total.

This is what linear regression does when we call fit. It tries to find the line whose squared vertical errors add up to the least.

## Slide 25: The fitted line is an equation

predicted cooling load = 22.6 + 0.426 × load_pct

A fit on load alone, to show the idea.
Intercept 22.6: the prediction when load is 0 percent.
Slope 0.426: each extra 1 percent of load adds 0.426 kW to the prediction.
At 70 percent load the line predicts 52.4 kW.
With both inputs the model learns one slope for each: 1.49 + 0.447 × load_pct + 0.756 × ambient_c. scikit-learn keeps these in intercept_ and coef_.

**Spoken script**

We keep saying a line, so let us write it down. A straight line is an equation with two numbers. The first is the intercept, where the line starts. It is the prediction when the load is zero. The second is the slope. It says how much the prediction rises for every extra one percent of load.

For our training rows the computer found an intercept of 22.6 and a slope of 0.426. So each extra percent of load adds about 0.43 kW to the cooling load. At seventy percent load the line predicts 52.4 kW. You can check that on a calculator.

Our real model has two inputs, load and ambient temperature, so it learns one slope for each. Those numbers are on the right. scikit-learn keeps them in two places, intercept underscore and coef underscore. Remember this slide. When we say the model learned something, we mean it found numbers like these.

## Slide 26: scikit-learn reads X as a table and y as a column

X has one row per observation and one column per feature. y holds one answer per row.

**Spoken script**

Before we call fit, we must hand scikit-learn the data in the shape it expects. On the left is our pandas table. The load and ambient columns are the features. They go into X, which is a grid with one row for each observation and one column for each feature. Here that is three rows and two columns, so we say its shape is three comma two. The target column goes into y. It is a single column of answers, one per row, so its shape is three with a comma and nothing after it. Underneath, pandas and scikit-learn both use a library called NumPy. NumPy stores numbers in arrays like these, and its shape tells you the rows and columns. When a model predicts, the answer it returns is also a NumPy array.

## Slide 27: NumPy arrays and their shape

np.array turns a list of numbers into an array.
A list inside a list gives rows and columns.
shape gives (rows, columns). One-dimensional y shows (rows,).
Later, a model's predict returns an array like this. Call .tolist() to get a plain Python list.

X has shape (3, 2) and y has shape (3,). Every row of X lines up with one entry of y.

```python
import numpy as np
X = np.array([[59.15, 31.71],
              [77.46, 29.97],
              [69.6, 19.87]])
y = np.array([52.547, 58.691, 47.895])
print(X.shape)
print(y.shape)
print(round(y.mean(), 3))
```

Output on the slide:

```text
(3, 2)
(3,)
53.044
```

**Spoken script**

Let us build the same arrays by hand. We import NumPy with the short name np. np.array turns a list of numbers into an array. A list of lists gives a grid, so X has three rows and two columns. y is a one-dimensional array of three numbers. The shape of X prints as three comma two. The shape of y prints as three with a comma and nothing after it, which means three entries and no second dimension. The mean of y is 53.044, in kW. Later, when we call predict, we will get an array back. If we want a plain Python list, for example to return from a function, we call dot tolist on it.

## Slide 28: Training walks downhill on the loss

Loss
One number for how wrong the model is. We use the mean squared error: square each miss, then average.
Gradient
Which way is downhill, and how steeply.
Learning rate
The size of each step. Too big overshoots; too small takes too long.
Gradient descent
Guess, measure the loss, step downhill, repeat.

Each orange dot is one try at the slope. The loss falls as the slope approaches the best value.

**Spoken script**

So far we said that a model learns from examples. Here is how the learning works. Imagine a model with one adjustable number, a slope. For every slope, we can measure how wrong the model is, and we call that number the loss. We use the mean squared error that we met a few slides ago. If we plot the loss against the slope we get a bowl. The bottom of the bowl is the best slope. We start from a poor guess, here a slope of zero, and we ask which way is uphill and how steep it is. That answer is called the gradient. We step the opposite way, downhill. The size of the step is the learning rate. Then we measure again and repeat. This repeated stepping is called gradient descent. The curve on the left comes from a tiny example where the best slope is exactly two, so you can see each try land closer to the bottom.

## Slide 29: Gradient descent in a few lines of NumPy

The best slope is 2, because y is always twice x.
w starts at 0. Each step moves it a little toward 2.
learning_rate sets the size of each step. np.mean averages an array. ** is the power from Week 3.
The loss falls on every step.

LinearRegression finds its line with a direct formula. Gradient descent is the walk behind neural networks, which we train in Semester 2.

```python
import numpy as np
x = np.array([1, 2, 3])
y = np.array([2, 4, 6])
w, learning_rate = 0.0, 0.05
print("step w loss")
for step in range(1, 6):
    gradient = 2 * np.mean(x * (w * x - y))
    w = w - learning_rate * gradient
    loss = np.mean((w * x - y) ** 2)
    print(step, round(w, 3), round(loss, 3))
```

Output on the slide:

```text
step w loss
1 0.933 5.31
2 1.431 1.51
3 1.697 0.43
4 1.838 0.122
5 1.914 0.035
```

**Spoken script**

Here is the same walk as code, using NumPy, the library from the last two slides. We have three points where y is always twice x, so the best slope is two. We start with a slope w of zero and a learning rate of zero point zero five. Inside the loop, the first line works out the gradient. For this loss it equals two times the average of x times the miss, and np dot mean is the NumPy tool that averages an array. You do not need to derive the formula now, because your calculus course shows where it comes from. The next line updates w by taking a step against the gradient, and the third line measures the loss, using the power symbol you met in Week 3. Look at the output. After one step w is 0.933, after two steps 1.431, and after five steps 1.914. The loss falls from 5.31 to 0.035. The model has learned the slope from the data, with nobody typing the number two. LinearRegression in scikit-learn finds its line with a direct formula, so it does not loop like this. We show the loop because neural networks learn by this kind of repeated downhill step, and in Semester 2 you will train one. The calculus you already know is what makes the gradient work.

## Slide 30: A model cannot learn from a blank, so we fill it first

An imputer fills each blank with the median of the training rows. Median means the middle value.

**Spoken script**

Before a model can learn, every input needs a number. In our training rows one ambient temperature is blank. That is row 14 in the picture. A model cannot add up a blank, so we fill it.

The usual fill is the median, the middle value you met in Week 6. The tool that does the filling is called an imputer. That word just means a filler.

The important detail is where the median comes from. We work it out from the training rows only. Here it is 26.07. We keep that number and reuse it for any blank in later rows. If we worked it out from the validation rows as well, the validation rows would leak a little information into the model, and the score would no longer be fair.

## Slide 31: A pipeline runs its steps in order

A pipeline is a short to-do list. Write it once, then call fit and predict on the whole list.

**Spoken script**

Now every row needs two jobs. First fill the blanks, then predict. A pipeline is a short to-do list that runs those jobs in order.

We write the list once with make underscore pipeline. When we call fit, the pipeline learns the median and then learns the model, both from the training rows. When we call predict, it fills the blanks in the new rows using the median it already learned, and then makes the prediction.

The benefit is safety. You cannot forget a step, and you cannot run the steps in the wrong order. In the next slides you will see the imputer and the model written as one pipeline.

## Slide 32: Training a model with missing inputs

training_data[feature_columns] selects the two input columns as a table. training_data["target"] selects the observed target as a Series.

SimpleImputer(strategy="median") learns input fill values from training rows. make_pipeline links that operation to LinearRegression. fit learns the steps and predict reuses them.

**Spoken script**

We now teach a model using the training rows, even though some inputs are blank.

Square brackets with the feature list select the two input columns as a table. Square brackets with the word target select the known answers as a single column, a Series.

Then we meet two tools from scikit-learn, the Python library for machine learning. SimpleImputer with strategy median learns a fill value for each input column, the middle value of the training rows. LinearRegression is the straight-line model. The make_pipeline function chains them into one list of steps, with the fill step first.

The fit function is the learning step. It lets each step study the training data. The predict function then applies what was learned to new rows, in the same order.

## Slide 33: Operations for the next example

Returning plain values: series.tolist() or array.tolist() returns a Python list of values, without pandas row labels. Preserve their order when pairing actual values and validation_predictions.

Rounded display: series.round(3) returns values rounded to three decimal places. Python round(number, 3) rounds one number. Keep unrounded calculations for returned assessment answers.

**Spoken script**

Two small helpers for showing results.

The tolist function turns a column or an array of values into an ordinary Python list, without the row labels. When we later put actual values next to predictions, keep both lists in the same order so each pair matches.

Rounding has two forms. Dot round three on a column rounds every value to three decimal places. The Python round function with a number and three rounds one value. Rounding is for display. When an assessed function returns an answer, keep the full unrounded calculation.

## Slide 34: A sequence of model steps / Filling model inputs

make_pipeline(imputer, estimator) links preprocessing and prediction. fit learns the imputer and estimator on training rows. predict applies the learned steps to new rows in the same order.

SimpleImputer(strategy="median") learns a median for each input column during fit. It uses those training medians to fill gaps later. Never learn replacement values from validation or test rows.

**Spoken script**

A pipeline is a short list of steps that run in order. Here we give make_pipeline an imputer and an estimator, which is simply the model that makes predictions.

When we call fit, each step learns from the training rows. When we call predict, new rows pass through the same steps in the same order, first filling blanks and then predicting.

The imputer is the first step. SimpleImputer with strategy median learns one median for every input column during fit, and later uses those training medians to fill any blank. Replacement values must always come from the training rows. Validation and test rows must never be used to learn them.

## Slide 35: Creating linear regression / Learning from training examples

LinearRegression() creates an unfitted model. It will learn coefficients and an intercept from training examples. Creating it alone does not train it or make predictions.

model.fit(input_table, observed_targets) learns model settings from paired rows. The two inputs must describe the same observations in the same order. Call fit before predict.

**Spoken script**

Creating a model and training it are two separate actions.

Writing LinearRegression followed by parentheses creates an empty model. Once it is fitted it will hold a slope for each input and an intercept, the starting value of the line. Before fit, it holds none of them. Creating it alone does nothing else.

The fit function does the learning. We give it the input table and the observed targets, row for row. Both must describe the same observations in the same order, because each row of inputs is paired with its answer.

Fit has to come before predict. Until a model has been fitted, it has nothing to predict with.

## Slide 36: Predicting new targets / Selecting a short preview

model.predict(input_table) returns one prediction per input row. Use the same feature columns and order as during training. Prediction uses learned settings; it does not refit the model.

values[:5] selects positions 0 through 4, or fewer if the sequence is shorter. The stop position is excluded. This preview does not change the full array stored in the variable.

**Spoken script**

Once a model is fitted, predict gives us its answers.

We pass the table of input columns, and we get back one predicted value for each row. Use the same feature columns, in the same order, as in training. Predict only uses the settings already learned, and it never refits the model.

To look at just a few predictions we use a slice. Writing values, square bracket, colon, five, closes the bracket, takes positions zero to four, so five values, or fewer if the sequence is shorter. The stop position of five is left out. A slice only previews. The full set of predictions stays unchanged in the variable.

## Slide 37: Standard names for model inputs

01

X_train: training input columns. y_train: the matching observed targets.

02

X_valid: validation input columns. y_valid: their observed targets, kept for evaluation.

03

Capital X usually means a two-dimensional table; lowercase y usually means one target per row.

**Spoken script**

Machine learning code follows a few standard names.

X underscore train holds the training input columns. y underscore train holds the matching known answers, one for each row of X underscore train.

X underscore valid holds the same input columns for the validation rows. y underscore valid holds their known answers. We keep these aside to judge the predictions afterwards.

Capital X is a table, with one row per observation and one column per feature. Lowercase y is a single column with one answer per row. These names are a habit that programmers share, and Python does not require them.

## Slide 38: Separate inputs from answers

X_train contains the input columns; y_train contains their observed targets.

X_valid contains the same input columns for validation; y_valid holds the answers for checking predictions.

Never include target among the inputs.

**Spoken script**

Every model needs two things kept apart, the inputs and the answers.

X underscore train contains the input columns of the training rows. y underscore train contains the known targets for those same rows, in the same order.

X underscore valid contains the same input columns for the validation rows. y underscore valid holds the validation answers. We use these only to check the predictions after they are made.

The target must never appear among the inputs. A model that is shown the answer as an input would copy it, and its error would look perfect without telling us anything useful.

## Slide 39: Training and predicting on the supplied data: step 1

X_train: input columns used for training.

Run the cell and read the output below it.

```python
X_train = training_data[feature_columns]
y_train = training_data["target"]
X_valid = validation_data[feature_columns]
y_valid = validation_data["target"]
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
```

**Spoken script**

This cell sets up the four pieces and loads three tools.

The first line selects the two feature columns from training_data and calls the result X underscore train. The second line selects the target column from the same rows, and calls it y underscore train. The third and fourth lines do the same for the validation rows.

Then three import lines bring in tools from scikit-learn. SimpleImputer fills blanks. make_pipeline chains steps together. LinearRegression is the straight-line model.

Importing a tool only makes it available. Nothing is trained here, and the cell prints no output.

## Slide 40: Create, then train, then predict

Creating an estimator sets up an empty model. fit learns settings from training inputs and their targets. predict uses those learned settings on new inputs; it does not learn from the validation targets.

**Spoken script**

Every model in scikit-learn follows the same three moves.

First we create it. Creating an estimator, which is the name for a model that learns and predicts, sets up an empty model with settings still unknown.

Second we train it with fit, giving it the training inputs and their targets. This is where it learns its settings.

Third we predict with new inputs. The model applies what it learned. It never looks at the validation targets while predicting, and that is what keeps the comparison fair.

## Slide 41: Training and predicting on the supplied data: step 2

X_train: input columns used for training.

Run the cell and read the output below it.

```python
linear_model = make_pipeline(
    SimpleImputer(strategy="median"), LinearRegression()
)
linear_model.fit(X_train, y_train)
validation_predictions = linear_model.predict(X_valid)
print(validation_predictions[:5].round(3).tolist())
```

**Spoken script**

Now the line model. We read it step by step.

The first statement builds a pipeline with two steps, a median imputer and then LinearRegression, and stores it as linear_model. The second statement calls fit on X underscore train and y underscore train. Here the imputer learns the training medians and the regression learns its slope for each input and its intercept.

The third statement calls predict on X underscore valid, and the result is one predicted value for every validation row, stored as validation_predictions.

The print line takes the first five predictions, rounds them to three decimal places, turns them into a list and shows them. They are predicted values of cooling load in kW, so check that they have a sensible size for that quantity.

## Slide 42: A decision tree asks yes or no questions

max_depth is a hyperparameter, a setting you choose before training. It limits how many questions in a row.

**Spoken script**

A decision tree is the second model we compare. It is a list of yes or no questions about the inputs. Read it from the top. Is the load at most 42.94 percent? If yes, go left. Otherwise go right.

The boxes at the bottom are called leaves. Each leaf predicts the average cooling load of the training rows that ended up there. This tree asks two questions in a row, so we say its depth is two.

The depth is a setting we choose before training. A setting like that is called a hyperparameter. In the assignment the tree may ask four questions in a row, so max depth is four. The other setting you will see, random state, fixes the starting point for any random choice inside the algorithm. With the same random state, everyone in the room gets the same tree.

## Slide 43: Baseline and tree comparisons

A mean baseline predicts the training target mean for every validation observation. A regression tree splits input space and predicts from training observations in each leaf.

Use the same training rows and validation rows for both. max_depth=4 limits tree depth and random_state=17 makes the example reproducible.

**Spoken script**

We compare two more methods on the same question.

The first is a mean baseline. For every validation row it predicts the average target of the training rows. It ignores the inputs completely, so it makes a useful yardstick. A model has to beat this to be worth using.

The second is a regression tree. It asks a series of yes or no questions about the inputs, which splits the rows into groups. Each group, called a leaf, predicts the average of the training rows that landed in it.

Both methods use the same training rows and the same validation rows. For the tree we set max_depth to four, which limits how many questions in a row. We set random_state to seventeen, so anyone who runs the code gets the same tree.

## Slide 44: A training-mean baseline / Creating a regression tree

DummyRegressor(strategy="mean") learns the mean training target during fit. It predicts that same value for every new row. Compare a more complex model against this simple baseline.

DecisionTreeRegressor splits inputs into regions with different predicted values. max_depth limits the number of split levels. random_state fixes random choices so the example can be repeated.

**Spoken script**

Two scikit-learn tools to introduce.

DummyRegressor with strategy set to mean is the baseline. When we call fit, it calculates the mean of the training targets. When we call predict, it gives that same value for every row. We compare every more complex model against it.

DecisionTreeRegressor is the tree. It learns questions about the inputs that split the rows into regions, and each region gets its own predicted value.

There are two settings. max_depth limits how many levels of questions the tree may ask. random_state fixes the random choices inside the method, so the example can be repeated and gives the same answer each time.

## Slide 45: Start with a simple reference

A training-mean baseline predicts the same value for every validation row. fit calculates that value from y_train.

Compare its error with the more complex model on the same validation rows.

**Spoken script**

A baseline is a simple reference prediction. The training-mean baseline gives the same value for every validation row.

That value comes from the fit step, which takes the average of y underscore train.

After that we measure the error of the more complex models on the same validation rows and compare it with the baseline error. If a model cannot do better than the plain average, it has learned nothing useful.

## Slide 46: Baseline and tree on the same CSV rows: step 1

baseline_model: a simple reference predictor which always predicts the training target mean.

Run the cell and read the output below it.

```python
from sklearn.dummy import DummyRegressor
from sklearn.tree import DecisionTreeRegressor
baseline_model = DummyRegressor(strategy="mean")
baseline_model.fit(X_train, y_train)
```

**Spoken script**

This cell creates the baseline and trains it.

The first two lines import tools from scikit-learn. DummyRegressor is the baseline model, and DecisionTreeRegressor is the tree we use in the next cell. The third line creates a baseline model with strategy mean and stores it as baseline_model. The fourth line calls fit with X underscore train and y underscore train.

During fit the baseline works out the mean of the training targets and stores it. That is all it learns.

The cell prints nothing. It only prepares the baseline for the comparison that comes next.

## Slide 47: Compare a second kind of model

A regression tree learns splits in the input columns. max_depth limits its split levels.

The imputer fills missing inputs using training medians; the tree then learns from those filled inputs.

**Spoken script**

Our second kind of model is the regression tree. It learns questions about the input columns, for example whether the load is above a certain value, and the answers split the rows into groups.

The setting max_depth limits how many levels of questions it may ask.

In the pipeline, the imputer runs first and fills blanks with the training medians. The tree then learns from the filled-in table.

## Slide 48: Baseline and tree on the same CSV rows: step 2

baseline_model: a simple reference predictor which always predicts the training target mean.

Run the cell and read the output below it.

```python
tree_model = make_pipeline(
    SimpleImputer(strategy="median"),
    DecisionTreeRegressor(max_depth=4, random_state=17),
)
tree_model.fit(X_train, y_train)
print(baseline_model.predict(X_valid)[:5].round(3).tolist())
print(tree_model.predict(X_valid)[:5].round(3).tolist())
```

**Spoken script**

This cell trains the tree and prints predictions from both models.

The first statement builds a pipeline in two steps. The imputer fills blanks with training medians, and then DecisionTreeRegressor with max_depth equal to four and random_state equal to seventeen learns the questions. We store it as tree_model, and the next line fits it on X underscore train and y underscore train.

The two print lines show the first five validation predictions, rounded to three decimals, from the baseline and from the tree.

The baseline list comes first. Every value in it is the same, because it always gives the training mean. The tree list varies from row to row, because different inputs fall into different leaves.

## Slide 49: Matching actual values and predictions

Every validation row has an actual target and its corresponding prediction. Subtract in the same order. abs() gives error magnitude.

MAE averages absolute errors. RMSE squares errors, averages them, then takes the square root. Both have the target’s unit.

**Spoken script**

To judge a model, every validation row needs two numbers. One is the actual target, the true recorded value. The other is the prediction for that same row.

The error is the actual value minus the prediction, taken in the same row order. The abs function gives the size of the error and drops its sign.

MAE stands for mean absolute error. We take the size of every error and average them. RMSE stands for root mean squared error. We square every error, average the squares, and take the square root. Both results come out in the unit of the target, which is kW, so they can be read directly as how far off we are.

## Slide 50: Operations for the next example

01

Adding or replacing a column: equipment_data["name"] = values assigns that column. An array follows row order. A Series aligns by row label, so keep labels paired with the intended observations.

02

Column arithmetic: Arithmetic on columns calculates one result per row. Series align by row label. Divide only where the denominator is valid and keep actual and predicted observations paired.

03

Mean of recorded values: series.mean() adds known values and divides by their count. pandas skips missing values by default. The result has the same unit as the original column.

**Spoken script**

Three operations that we need for the error calculation.

Assigning a column. Writing the table name, then a new column name in square brackets, then equals and a set of values, adds that column or replaces it. If the values are an array, they follow row order. If they are a Series, they line up by row label. So make sure each value is attached to the right observation.

Column arithmetic. Subtracting one column from another works row by row and gives one result per row.

The mean function adds the recorded values and divides by how many there are. By default pandas skips missing values. The result is in the same unit as the column, so an average of errors in kW is itself in kW.

## Slide 51: Operations for the next example

Magnitude of each error: series.abs() makes negative values positive while leaving nonnegative values unchanged. Averaging these magnitudes gives mean absolute error.

**Spoken script**

One more tool for measuring errors. The abs function turns every negative number into a positive one and leaves positive numbers and zero as they are.

An error of minus two and an error of plus two are equally big misses, and abs treats them that way. If we average these sizes, we get the mean absolute error, the average distance between predictions and actual values.

## Slide 52: Squared error and square root

error ** 2 squares each error. After averaging, ** 0.5 takes the square root. This gives root mean squared error, which penalises large errors more strongly than mean absolute error.

**Spoken script**

Squaring and square roots give us the second error measure.

In Python, a double asterisk means to the power of. So error, double asterisk, two, squares each error. Squared errors are always positive, and a large miss becomes much larger than a small one.

We average the squared errors, and then double asterisk zero point five takes the square root. The square root brings the result back to the unit of the target, which is kW.

The outcome is root mean squared error, or RMSE. Because squaring makes large misses weigh heavily, RMSE reacts more strongly to big errors than the mean absolute error does.

## Slide 53: Line up observations and predictions

Copy record IDs and observed targets from validation rows.

Add predictions in that same order.

Each row now pairs one observation with its own predicted value.

**Spoken script**

To calculate errors we first put each actual value next to its prediction.

We copy the record IDs and the observed targets from the validation rows into a new table. Then we add the predictions as a new column, in the same order as the validation rows.

Each row of this table now holds one observation and the prediction made for that same observation. That pairing is what lets us subtract one from the other in the next step.

## Slide 54: Errors from the supplied validation observations: step 1

validation_results: actual and predicted targets paired with each record ID.

Run the cell and read the output below it.

```python
validation_results = validation_data[
    ["record_id", "target"]
].copy()
validation_results["predicted"] = validation_predictions
```

**Spoken script**

This cell builds the table that pairs answers with predictions.

The first statement selects two columns from validation_data, record_id and target, and makes a copy, called validation_results. The list of two names in double square brackets gives a table with just those columns.

The second statement adds a new column called predicted and fills it with validation_predictions, the predictions from the line model. Because we give it an array, the values go in row order, and each prediction lands next to the row it was made for.

Nothing is printed. The table is ready for the error calculation in the next cell.

## Slide 55: Measure how far predictions missed

Subtract predicted from observed values.

Positive errors mean underprediction; negative errors mean overprediction. abs removes signs for MAE.

Squaring before averaging and taking a square root gives RMSE.

**Spoken script**

We measure each miss by subtracting the prediction from the observed value.

A positive result means the model predicted too low, an underprediction. A negative result means the model predicted too high, an overprediction.

For the mean absolute error, abs removes those signs before we average. For RMSE, we square the errors, average the squares and take the square root. Both end up as one number in kW, and a smaller number means predictions closer to the truth.

## Slide 56: Errors from the supplied validation observations: step 2

validation_results: actual and predicted targets paired with each record ID.

Run the cell and read the output below it.

```python
prediction_errors = (
    validation_results["target"] - validation_results["predicted"]
)
mae = prediction_errors.abs().mean()
rmse = (prediction_errors**2).mean() ** 0.5
print(validation_results.head())
print(round(float(mae), 4), round(float(rmse), 4))
```

**Spoken script**

This cell computes both errors, line by line.

The first statement subtracts the predicted column from the target column, row by row, and stores the differences as prediction_errors. The second statement takes abs of each difference and then the mean, which gives mae. The third statement squares each error with a double asterisk two, takes the mean, and raises that to the power of zero point five, a square root, which gives rmse.

The first print shows the first five rows of validation_results, so we can see actual and predicted values side by side. The last print shows mae and rmse, converted to ordinary numbers and rounded to four decimals.

Both values are in kW. RMSE is at least as large as MAE, and the gap grows when a few errors are large.

## Slide 57: One MAE for each model on the validation rows

A dictionary pairs each name with a model we fitted earlier.
items() gives one name and one model per turn of the loop.
mean_absolute_error(actual, predicted) is the MAE from earlier slides.

The numbers are in kW. Each model predicts the same validation rows.

```python
from sklearn.metrics import mean_absolute_error
models = {
    "baseline": baseline_model,
    "line": linear_model,
    "tree": tree_model,
}
for name, model in models.items():
    predicted = model.predict(X_valid)
    error = mean_absolute_error(y_valid, predicted)
    print(name, round(error, 2))
```

Output on the slide:

```text
baseline 9.69
line 0.74
tree 3.39
```

**Spoken script**

We now have three fitted models, so let us score them all in the same way. The dictionary pairs a short name with each model we fitted earlier. The loop takes one name and one model at a time. For each model we predict the validation rows, and then we score the predictions with mean absolute error, the MAE we calculated by hand.

Look at the three printed lines. Each one is the average miss of one model, in kW. They all use the same validation rows, so the comparison is fair.

## Slide 58: Three models on the validation rows

The line misses by about 0.74 kW on average. The average guess misses by 9.69 kW.
All three models used the same training rows and the same validation rows.

**Spoken script**

Here is what everything we built today produces, on the validation rows that none of the models saw. The average guess misses by 9.69 kW on average. The tree misses by 3.39. The line misses by 0.74.

Look at the pattern. The line beats the tree by a wide margin. Remember the scatter plot: the dots follow a straight path, so a straight line is the right shape. A tree can only predict in steps, so it has to cut that path into rough pieces.

A more complicated model earns its place only when the error falls. Always put the baseline beside the number, and let the simplest model that does the job win.

## Slide 59: Pandas inside the required function

The assignment caller supplies equipment_records. pd.DataFrame(records) gives those records named columns. Calculate with pandas, then return the published Python type.

to_dict("records") makes a list of row dictionaries. Series.tolist() makes a list of values. A grouped Series.to_dict() maps group labels to their values.

**Spoken script**

For the assignment, your code goes inside functions. Each function receives its data as an input.

The assignment caller supplies equipment_records, which is a list of row dictionaries, where each dictionary is one row. The call pd dot DataFrame with that list turns it into a table with named columns. Then we calculate with pandas and return the Python type the task asks for.

Three conversions help with that. The to_dict function with the word records gives a list of row dictionaries. The tolist function on a Series gives a plain list of values. And to_dict on a grouped result gives a dictionary that maps each group label to its value.

## Slide 60: Operations for the next example

01

Returning a dictionary: series.to_dict() maps Series labels to values. equipment_data.to_dict("records") instead returns a list of row dictionaries. Choose the form required by the assignment.

02

A table from Python values: pd.DataFrame(records) builds a table from row dictionaries. With a dictionary of column lists, keys become column names and each list supplies that column’s values.

03

Grouping rows: equipment_data.groupby("label")["value"] groups the value column by matching labels. Apply mean() or sum() to calculate one result per group. Missing group labels are excluded by default.

**Spoken script**

Three operations for the function example.

First, to_dict. On a Series, it gives a dictionary that maps each label to its value. On a whole table, to_dict with the word records gives a list of row dictionaries. Use whichever form the assignment asks for.

Second, pd dot DataFrame with a list of row dictionaries builds a table. If we give a dictionary of column lists instead, each key becomes a column name and each list fills that column.

Third, groupby. Writing groupby with a column name, then a value column in square brackets, splits that value column into groups with matching labels. Then calling mean or sum gives one result for each group. Rows with a missing group label are left out by default.

## Slide 61: Defining and calling a function

def gives a reusable block a name and input parameters. The indented statements run when it is called. return sends a result back to the caller; print displays a result but does not return it.

**Spoken script**

A function is a block of code with a name that we can run again whenever we need it.

The word def starts the definition. After it come the function name and the parameters, the names for the inputs it will receive. The indented lines underneath are the body, and they only run when we call the function.

The return statement sends a result back to whoever called the function. The print function shows a value on the screen but sends nothing back. An assessed function must use return, because the grader reads the returned value.

## Slide 62: A function called with the supplied records

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

This example is a complete function, and then a call to it.

The def line names the function mean_load_by_equipment and gives it one input, equipment_records. The first line inside builds a table from those records. The second groups the rows by equipment_id, picks the load_pct column and takes the mean for each group. The last line returns that result as a dictionary, with each equipment ID as a key.

Below the function, we turn modelling_data into a list of row dictionaries with to_dict and the word records. We call the function with that list and print what it returns.

The output is a dictionary with one average load for each piece of equipment, so check that every equipment ID appears once.

## Slide 63: Words from today

**Spoken script**

Let us gather today's new words in one place. A baseline is the simple guess every model must beat. An error is the actual value minus the predicted value. MAE is the average size of the misses, and RMSE is a similar score that punishes large misses more. Loss is the single number that training tries to lower. An imputer fills blanks, and a pipeline runs steps in order. A hyperparameter is a setting you choose before training, such as the depth of a tree.

Keep this slide. Every one of these words returns in the next weeks.

## Slide 64: Your issued task

01

Investigate building cooling load.

02

Target units: kW.

03

These are synthetic teaching records for practice.

04

Each record is one operating observation; equipment_id repeats across observations.

**Spoken script**

Your task this week is to investigate cooling load. The target is measured in kW, so every error you report is in kW.

Each record is one operating observation, one reading of a machine at a moment. The equipment_id repeats across observations, so many rows belong to the same piece of equipment.

These are synthetic teaching records, made up for learning. They are good for practising the method and are unsuitable for running real equipment.

## Slide 65: predict_regression(training_records, feature_records)

Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only.

Return three prediction lists under baseline, linear and tree.

Feature records have no target.

Fit preprocessing only on training data.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The first function you write is predict_regression. It takes two inputs. The first is training_records, a list of rows that include the target. The second is feature_records, a list of rows that have no target, and these are the rows to predict.

Inside the function you fit three models on the training rows. They are the training-mean baseline, linear regression and a decision tree with max_depth equal to four and random_state equal to seventeen. All three use only load_pct and ambient_c as inputs.

The imputer that fills blanks must learn its medians from the training data alone.

The function returns a dictionary with three keys, baseline, linear and tree. Each key holds a list of predictions, one for each feature record. Keep the names exactly as written, and check the types and the units against your brief.

## Slide 66: regression_errors(actual, predicted)

Return mae and rmse, calculated over the same paired observations, with full precision.

Keep the exact names and outputs. Check types, units and the issued brief.

**Spoken script**

The second function is regression_errors. It takes two inputs. The first is actual, the list of true target values. The second is predicted, the list of predictions for the same observations in the same order.

It returns a dictionary with two keys, mae and rmse. The first holds the mean absolute error and the second the root mean squared error.

Both must be calculated over the same paired observations, so the first prediction goes with the first actual value, and so on down the lists. Return the full precision numbers with no rounding. Keep the exact names, and check the types and units against your brief.

## Slide 67: Written evidence

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

First, explain the supplied scenario in your own words. Say what was being predicted and what the inputs were.

Second, state the unit of the target, give your reasons for your choices, and describe the limits of what you did. For example, you can say why the fill values came from the training rows only.

The code and the written evidence go in one complete notebook, and you submit that single notebook.

## Slide 68: Regression and baseline submission

01

Opens: 27 Oct 2026, 11:00 Kampala

02

Deadline: 03 Nov 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open W08 assignment form

https://docs.google.com/forms/d/e/1FAIpQLSfOpt4U_rhJrjlYCp6pyzm9ygu2vN5EwO9yeAiJaUKy-kJKoA/viewform

**Spoken script**

This slide covers this week's assignment submission, the regression and baseline notebook.

Check the opening time, the deadline and the form link on the slide. When you open the form, enter your full Student Registration Number, so your work is matched to you.

Submit one complete notebook, then wait until the file name appears before you press Submit. Keep the submitted files and the confirmation message you receive, as your proof that the work went in.

## Slide 69: Week 8 quiz

01

Answer individually after the lecturer activates the quiz.

02

Available for 24 hours from activation.

03

Use your Student Registration Number and registered account.

04

Check the announced quiz closing time.

Open this week’s quiz

https://forms.gle/MKAfeSE9NfRziGebA

**Spoken script**

Next comes the Week 8 quiz. You answer it individually.

The quiz opens when the lecturer activates it, and it then stays open for twenty-four hours. Use your Student Registration Number and your registered account when you fill in the form. Check the announced closing time on the slide, so you know when it ends.

## Slide 70: Revision and submission checklist

Explain to a classmate what a feature and a target are in today's data, why some rows stay hidden while a model learns, and what an error of 0.74 kW tells you.

Keep raw data unchanged. Restart and run all cells before submitting the required assignment notebook.

Point to your evidence. Save your work.

**Spoken script**

Before you leave, check yourself with this exit task. Explain to a classmate what a feature and a target are in today's data. Then explain why some rows stay hidden while a model learns. Finally, say what an error value in kW tells you about the predictions.

To submit, keep the raw data unchanged. Restart the notebook and run all the cells from the top, so you know the whole notebook works in order, and then submit the required assignment notebook.

Be ready to point to the evidence in your notebook for each answer, and save your work.

## Slide 71: Optional revision video

01

For revision after class.

02

StatQuest with Josh Starmer
The Essence of Linear Regression!!!

03

Opening up to 04:00, optional preview-selected excerpt

04

Listening question: How can a fitted line turn an input into a numerical prediction?

Open explainer video

https://www.youtube.com/watch?v=aFDOzpTeg0s

**Spoken script**

For revision after class, there is an optional video from StatQuest with Josh Starmer, called The Essence of Linear Regression. Watch the opening four minutes.

As you watch, keep one question in mind. How can a fitted line turn an input into a numerical prediction? That is the idea behind the line model we built today.

The link is on the slide. The video is for revision, and you can watch it in your own time.
