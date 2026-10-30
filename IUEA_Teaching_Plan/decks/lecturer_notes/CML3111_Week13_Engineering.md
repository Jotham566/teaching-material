# CML3111 Week 13

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Making the project understandable and runnable

Communications, Electrical, Mechatronics and Robotics Engineering

Friday 04 December 2026
Friday 11:00–14:00, Room 115

**Spoken script**

Welcome to Week 13 for CML3111, Communications, Electrical, Mechatronics and Robotics Engineering.

By now we have built models and charts for our project. This week we make that work something another person can open and run. We will learn how to describe our project so a stranger can follow it, and how to check for ourselves that it really runs from the start. The day, time and room are on the slide.

## Slide 2: Today’s learning

Hold a flexible model back with a penalty and predict from the nearest neighbours.
Compare five candidates fairly.
Make the project run for someone else, from a clean start.

You can say what regularisation, alpha and k mean, and read a table of candidates.
Another learner can follow your written instructions and reproduce your stated result.

**Spoken script**

Today has two halves. In the first half we finish our tour of modelling. We learn to hold a flexible model back with a penalty, which is called regularisation, and we meet a model that predicts from the nearest neighbours. Then we compare five candidates fairly. In the second half we turn to the project. We make it runnable by someone else from a clean start, because a result that nobody else can reproduce is hard to trust. By the end you can say what regularisation, alpha and k mean, read a table of candidates, and follow your own written instructions to reproduce your results from a clean start.

## Slide 3: Words for today: holding a model back

**Spoken script**

Six words for the first half of today. Regularisation means holding a model back, so that it cannot chase every wobble in the training rows. The usual way is a penalty, an extra cost added to the loss whenever the coefficients get large. Ridge regression is a line or a curve fitted with exactly that kind of penalty. The setting alpha says how strong the penalty is, and, like the depth of a tree, it is a hyperparameter that we choose before training.

A polynomial feature is a power of an input, such as load squared or load cubed. Adding powers gives a straight-line method room to bend, and a flexible curve often needs holding back. Lasso is a cousin of ridge that can push some coefficients all the way to zero. We only name it today.

## Slide 4: Preparing the rows once more

The same cleaning as Weeks 8 to 12: drop copies, keep valid rows.
E1 to E4 train, E5 validates, E6 stays sealed.
X holds the two inputs. y holds the target.

Every experiment today uses these four tables.

```python
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_absolute_error
raw = pd.read_csv("engineering_data.csv")
data = raw.drop_duplicates("record_id")
data = data[data["target"].notna()
            & data["load_pct"].between(0, 100)].copy()
groups = ["E1", "E2", "E3", "E4"]
train = data[data["equipment_id"].isin(groups)]
valid = data[data["equipment_id"] == "E5"]
features = ["load_pct", "ambient_c"]
X_train, y_train = train[features], train["target"]
X_valid, y_valid = valid[features], valid["target"]
print(len(train), len(valid))
```

Output on the slide:

```text
58 15
```

**Spoken script**

Before the experiments, we set up the same tables as in the last weeks. We read the file, drop repeated record IDs, and keep the rows that have a target and a valid load. Then we pick out the training rows, the equipment groups E1 to E4, and the validation rows, which are E5. The last group, E6, stays sealed.

X holds the two inputs, load and ambient temperature. Y holds the target, which here is motor temperature. The last line prints the sizes: 58 training rows and 15 validation rows. Every experiment today uses these four tables.

## Slide 5: A flexible curve can chase the training rows, and a penalty calms it

Same degree-6 curve on load alone. Left: no penalty. Right: penalty alpha = 1.

**Spoken script**

Here is a curve built from the powers of load, up to load to the power of 6. That gives a straight-line method a lot of room to bend. On the left there is no penalty, so the curve is free to chase the training rows, the dark dots. On the right we add a penalty with alpha equal to one, and the curve calms down.

The orange diamonds are the validation rows. They are the honest test of each curve, because neither curve has seen them. Notice that the penalised curve is smoother, and that its error on the training rows is slightly larger than the free curve's error. We accept a slightly worse fit to the training rows in exchange for a more stable model.

## Slide 6: Ridge adds a price for large coefficients

loss = sum of squared misses
+ alpha × (sum of squared coefficients)

alpha = 0 means no penalty. The method is ordinary least squares.
A larger alpha shrinks the coefficients toward zero and calms the curve.
We choose alpha with the validation rows, in the way that we chose tree depth.
The penalty treats all coefficients alike, so the inputs are scaled first. That is why StandardScaler sits in the pipeline.

**Spoken script**

Here is the whole idea in one line. Training lowers a loss, and the loss we know is built from the squared misses. In scikit-learn's Ridge we add up the squared misses over all the training rows. Ridge then adds a second part: alpha times the sum of the squared coefficients. A model can now lower its loss in two ways, by fitting the data better, or by making its coefficients smaller. The starting level of the line, the intercept, is left out of the penalty.

When alpha is zero there is no penalty, and we are back to ordinary least squares. A larger alpha pushes the coefficients toward zero and calms the curve. We choose alpha the same way we chose the depth of a tree, by looking at the validation rows.

One practical detail. The penalty adds up the squares of all coefficients and treats them alike, so the inputs must be on a common ruler first. That is the reason StandardScaler appears in the pipeline on the next slide.

## Slide 7: Three curve models that differ only in the penalty

PolynomialFeatures(6) adds load squared up to load to the power of 6.
StandardScaler puts those columns on a common ruler.
The last step is the estimator: no penalty, alpha 1 or alpha 100.

A dictionary keeps the three models side by side. Nothing is fitted yet.

```python
from sklearn.preprocessing import (
    PolynomialFeatures, StandardScaler)
from sklearn.linear_model import LinearRegression, Ridge
def curve_model(estimator):
    return make_pipeline(
        PolynomialFeatures(6, include_bias=False),
        StandardScaler(), estimator)
models = {
    "none": curve_model(LinearRegression()),
    "alpha 1": curve_model(Ridge(alpha=1)),
    "alpha 100": curve_model(Ridge(alpha=100)),
}
```

Output on the slide:

```text
(nothing printed)
```

**Spoken script**

Now the code. The function curve model builds one pipeline from three steps. The first step, PolynomialFeatures with six, adds the powers of the input: load, load squared, up to load to the power of six. The second step, StandardScaler, puts those columns on a common ruler. The third step is the estimator we pass in.

The dictionary below keeps three versions side by side. The first uses LinearRegression, which has no penalty. The second uses Ridge with alpha equal to one. The third uses Ridge with alpha equal to one hundred. Nothing is fitted yet. The pipelines are recipes.

## Slide 8: Fitting the three curves and scoring them

X_train[["load_pct"]] keeps the load column only, as a table.
Each model is fitted on the training rows and scored on both sets.
Errors are in deg C.

A stronger penalty lowers the fit to the training rows. The validation rows say whether that helps.

```python
load_train = X_train[["load_pct"]]
load_valid = X_valid[["load_pct"]]
print("model train valid")
for name, model in models.items():
    model.fit(load_train, y_train)
    train_pred = model.predict(load_train)
    valid_pred = model.predict(load_valid)
    train_mae = mean_absolute_error(y_train, train_pred)
    valid_mae = mean_absolute_error(y_valid, valid_pred)
    print(name, round(train_mae, 2), round(valid_mae, 2))
```

Output on the slide:

```text
model train valid
none 4.02 4.6
alpha 1 4.16 4.2
alpha 100 5.82 6.87
```

**Spoken script**

Now we fit the three models and score each one twice, on the training rows it learned from and on the validation rows it has never seen. We keep only the load column, because the curve is built from powers of load alone.

Read the three printed lines. With no penalty the training error is 4.02 and the validation error is 4.60. With alpha equal to one they are 4.16 and 4.20. With alpha equal to one hundred they are 5.82 and 6.87.

The penalty of one improved the validation error, which suggests that holding the curve back helped. A penalty of one hundred is too strong, and both errors rise, because the curve is held so tightly that it can no longer follow the pattern.

## Slide 9: What the penalty does to the coefficients and the errors

A plain straight line on load alone: validation MAE 4.30 deg C.
The Week 8 line on load and ambient temperature: 0.78 deg C.
In scikit-learn the coefficients are in model[-1].coef_, the last step of the pipeline.

**Spoken script**

Look at the second column. Without a penalty, the largest coefficient on the scaled columns is over 10,000. These huge coefficients cancel each other out to draw a wiggly curve. With alpha equal to one the largest coefficient shrinks to 10.8, and with alpha equal to one hundred to 2.6.

That is shrinkage. The penalty keeps all coefficients small, and a model with small coefficients is much less able to swing between training rows. For comparison, a plain straight line on load alone scores 4.30 deg C on the validation rows. The best curve here scores 4.20, so with only fifteen validation rows the two are too close to separate. The big gain comes from a better input: the Week 8 line with both load and ambient temperature scores 0.78.

## Slide 10: Words for today: predicting from neighbours

**Spoken script**

Five words for the second half. A neighbour is a training row whose inputs are close to the inputs of a new row. Distance says how close, measured over all the inputs, and for this to be fair the inputs must be scaled first. The number k says how many neighbours we use. K nearest neighbours, written KNN, predicts by averaging the targets of the k closest training rows. People call it a lazy learner, because it stores the training rows and does its work only when a prediction is asked for.

## Slide 11: A prediction from the three nearest training rows

The star is the validation row with record_id 5. Its 3 nearest training rows (scaled inputs) have targets 65.441, 70.592 and 74.039.

**Spoken script**

Here is KNN at work. The star is one validation row, the one with record_id 5. The grey dots are the training rows. To predict, we find the three training rows closest to the star, which are the green dots. Their targets are 65.441, 70.592 and 74.039, all in deg C.

The prediction is their average, 70.0 deg C. The true value for this row is 67.034, so the miss is 3.0. Distances are measured after scaling both inputs, so a step of one typical swing in load counts the same as a step of one typical swing in ambient temperature. The picture uses the scaled columns, so the nearest rows really are the nearest on the page.

## Slide 12: Trying three values of k

n_neighbors is k, the number of neighbours that vote.
The imputer fills blanks and the scaler puts inputs on a common ruler before distances are measured.
Errors are in deg C, on the validation rows.

fit stores the training rows. predict does the neighbour search.

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
print("k valid")
for k in [1, 3, 20]:
    model = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        KNeighborsRegressor(n_neighbors=k))
    model.fit(X_train, y_train)
    valid_pred = model.predict(X_valid)
    valid_mae = mean_absolute_error(y_valid, valid_pred)
    print(k, round(valid_mae, 2))
```

Output on the slide:

```text
k valid
1 2.42
3 1.58
20 5.55
```

**Spoken script**

The pipeline has three steps. The imputer fills the one blank ambient temperature in the training rows, using the median, which is the middle value. The scaler puts load and ambient temperature on a common ruler, because KNN measures distance and an unscaled input with big numbers would dominate. The last step is the KNN regressor, and n neighbors is the number we called k.

The loop tries three values of k and prints the validation error for each. Read the three lines. With k equal to 3 the error is 1.58 deg C, the lowest of the three. With k equal to one the model copies a single neighbour, noise included. With k equal to twenty it averages so many rows that the prediction becomes blurry. As with tree depth, a small value chases noise and a very large value misses the pattern.

## Slide 13: Choosing k, and the price of waiting until prediction time

CHOOSING k
Try several values and compare the validation error. Very small k chases noise. Very large k averages too much.
Here k = 3 gives the lowest error of the three we tried.

THE PRICE
KNN keeps every training row. Each prediction measures the distance to all of them, so it slows down as the training table grows.
A line or a tree answers in an instant once it is trained.

**Spoken script**

How do we choose k? We do what we did for tree depth and for alpha: try several values and compare the validation error. A very small k chases noise. A very large k averages too much and blurs the pattern. In our rows k equal to 3 gave the lowest error of the three values we tried.

There is a price to remember. KNN keeps every training row. For each prediction it measures the distance to all of them, so it gets slower as the training table grows. A line or a tree is quick to answer once trained. For a small engineering table the difference is invisible, and for a million rows it matters.

## Slide 14: Five candidates on the same validation rows

All five were scored on the same validation rows.
The ridge row sees load only, so it is not a like-for-like comparison.
alpha and k were chosen on these rows, so the scores are slightly optimistic.

**Spoken script**

Here are five candidates scored on the same validation rows, with the baseline at the top. The average guess is the reference. The straight line using both inputs scores 0.78. The depth four tree scores 4.79. The ridge curve on load alone scores 4.20. KNN with k equal to three scores 1.58.

The straight line on both inputs fits these rows best, and KNN on the same two inputs comes second. The ridge curve sees only the load, so its row is not a like-for-like comparison. A flexible model earns its place only when the pattern needs it. When two models score about the same, we choose the simpler one, because it is easier to explain and to maintain. One caution: we picked alpha and k by looking at these same validation rows, so these scores are slightly optimistic. The sealed test group gives the final check later. We will use this reasoning in the project write-up.

## Slide 15: Which model for which job

**Spoken script**

To close the modelling block, here is a quick guide to which model for which job. A straight line works well when the pattern is close to a straight path, and it fails on curves. Ridge suits flexible or crowded inputs where overfitting is a risk, and it needs scaling and a sensible alpha. A decision tree handles inputs that interact, and its answers can be jumpy. A random forest smooths a jumpy tree and gives up some clarity. KNN works when nearby rows really are similar, and it needs scaling and gets slow on big tables.

No row in this table is the best everywhere. We choose with evidence from validation rows, and we explain the choice.

## Slide 16: Words from today

**Spoken script**

Six words to keep from the modelling half. Regularisation holds a model back with a penalty. Alpha is the strength of that penalty. Shrinkage is what the penalty does to the coefficients. A neighbour is a close training row and k is how many we use. KNN averages the targets of the k closest rows. Alpha and k are both hyperparameters, settings we choose before training. Shrinkage and neighbours lead into the second half of today, where we make the project runnable by someone else.

## Slide 17: Connection to the previous lesson

The models and charts already exist.

The remaining task is to make the evidence understandable and runnable from the supplied files.

**Spoken script**

Let us connect to where we stopped last time.

Our models already exist, and so do our charts. The hard modelling work is done. What remains is a different kind of job. We must make the evidence understandable to someone who was not sitting next to us, and we must make it runnable from the files we hand over.

Think of it as packing a toolbox for a colleague. The tools are made. Now we label them and check the colleague can open the box and use them.

## Slide 18: The continuing pandas workflow

Load CSV files with pd.read_csv. Keep raw data unchanged and use named columns throughout the investigation.

Use pandas for cleaning, summaries and model inputs. Return the published Python types at assessment function boundaries.

**Spoken script**

First, a quick revision of the pandas habits we already have.

We load a CSV file with pd dot read underscore csv. We keep the raw data exactly as it arrived and never edit that original. Throughout the investigation we refer to columns by their names, so the code reads clearly.

We use pandas for cleaning the data, for making summaries and for preparing the inputs to our models. When we write a function for an assessment, we return the Python types that the published instructions ask for. This is revision only. Nothing new is being added to the test.

## Slide 19: Relative data paths and saved outputs

pd.read_csv("data/raw/engineering_data.csv") reads a file relative to the notebook’s working folder. State that folder in the README.

clean.to_csv("cleaned_data.csv", index=False) exports a table without adding pandas row labels as a new column.

**Spoken script**

Two lines of code matter for handover, so we read them slowly.

The first is pd dot read underscore csv, with the text data slash raw slash engineering underscore data dot csv. A path is the address of a file. This one says to look in a folder called data, then a folder inside it called raw, and find the file there. The address starts from the working folder of the notebook, which is the folder where the notebook is currently running. So the README must say which folder that is.

The second is clean dot to underscore csv, with the name cleaned underscore data dot csv, and index equals False. It saves our table as a file. Setting index to False stops pandas from adding its row numbers as an extra column in the saved file.

## Slide 20: Why this week’s tools are needed

A project is ready for handover when its files and written instructions reproduce its results in a fresh session.

Check each claim against the results in your notebook.

**Spoken script**

Why do we need these tools this week?

We say a project is ready for handover when its files and its written instructions reproduce its results in a fresh session. That is a clear test. We hand the work over, someone starts from nothing, follows our words, and gets our results.

While we prepare, we check each claim we make against the results in our notebook. If we write that a model reached a certain score, the notebook must show that score when it runs. A claim with nothing behind it weakens the whole project.

## Slide 21: Reproducibility and Dependency

Reproducibility

Another person can use the stated data, environment and steps to check the result. Terminology varies; state the test you used.

Dependency

A package your code needs. Record versions actually used, rather than guessing them.

**Spoken script**

Two words to define before we go further.

Reproducibility means another person can take our stated data, our stated software setup and our stated steps, and get the same result we reported. People use this word in slightly different ways, so in our README we say exactly what we mean by getting the same result.

A dependency is a package our code needs in order to run. Pandas is a dependency. Scikit-learn is another. When we record dependencies, we write down the versions we actually used. We look them up, because a guess might be wrong, and a wrong version can make the code behave differently on someone else's machine.

## Slide 22: Relative path and README

Relative path

A location interpreted from the current working folder. It is not always relative to the notebook file itself.

The project’s instructions: question, files, data source, environment, run order, results and limitations.

**Spoken script**

Now two more terms.

A relative path is a file location that is read from the current working folder. If our working folder holds a folder called data, the relative path data slash readings dot csv leads to the readings file inside it. In some tools the working folder is a different place from the folder that holds the notebook, so we always check where we are running.

A README is the instruction page for the project. It tells a newcomer the question we are answering, the files included, where the data came from, the software needed, the order to run things, the results, and the limitations. If someone can read only one file, this is the one we want them to read.

## Slide 23: A useful README

01

State the engineering question and target unit.

02

List the supplied data and required software versions.

03

Give the order for running the notebook from a fresh session.

04

State limitations and each member’s contribution.

**Spoken script**

Here is what a useful README holds, in four parts.

First, we state the engineering question and the unit of the target. For example, we write that we predict motor temperature in deg C, and we write which one.

Second, we list the data supplied and the software versions needed.

Third, we give the order for running the notebook from a fresh session. Open this file, load this data, run the cells from top to bottom.

Fourth, we state the limitations of our work and what each team member contributed. The README is written for someone opening the project for the first time, so we choose specific words. Instead of saying run the analysis, we name the notebook and the data file to use.

## Slide 24: Someone else needs to reproduce the result

Which instructions would a new user need?

**Spoken script**

Let us picture a real situation. Someone else has our project folder, and they must reproduce our result. We will not be there to answer questions.

Take a minute and think about what that person needs from us. What do they need to know to open the files, put the data in the right place and run the notebook in the right order?

Keep your list, because the next slides show how a clean restart tests whether our instructions are good enough.

## Slide 25: A reproducible notebook starts fresh

The saved outputs must agree with a fresh run in the stated order.

**Spoken script**

A reproducible notebook can start from a fresh session and still give the answers it shows.

When we work, our notebook builds up variables in memory. Cells that we ran earlier, or even deleted, may still leave their effects behind. The saved outputs on the page can then look right while the code underneath could no longer produce them.

So the test is simple. We restart the session, run the cells in the order the README states, and compare what appears with the saved outputs. If they agree, the notebook passes our fresh-start check. If they differ, we have found something to fix.

## Slide 26: Saved outputs can hide missing steps

01

A notebook can display an old answer after its inputs have changed.

02

A fresh session begins without the old variables.

03

Restarting and running all tests whether the stated order creates the result.

**Spoken script**

Why are saved outputs risky? Three points.

One. A notebook can display an old answer even after its inputs have changed. The number on the screen was produced earlier and nothing refreshed it.

Two. A fresh session starts without any of the old variables. Anything the code relied on, but which we forgot to create in a cell, will be missing.

Three. Restarting and running all the cells tests whether the stated order really creates the result. If a cell fails with a name error, we have found a missing step. That is a useful discovery, because we can fix it before anyone else meets it.

## Slide 27: A path names where a file is found

01

A relative path is interpreted from the current working folder.

02

Package versions describe the software used to run the code.

03

The README must give both run instructions and data-access instructions.

**Spoken script**

Three ideas about paths and versions.

One. A relative path is read from the current working folder. So a path like data slash readings dot csv works on any computer, on any computer, as long as the person is running from the right folder.

Two. Package versions describe the software we used to run the code. Different versions can give different behaviour, so we record them.

Three. The README must give two kinds of instruction. It must say how to run the project, and it must say how to get the data. If the data is large or private, the README tells the reader where to obtain it and where to place it.

## Slide 28: Read the path example

Path and cwd

Path is a tool imported from Python’s pathlib module. Path.cwd() returns the folder where Python is currently running.

name

The .name property gives the last folder component as text. It depends on your runtime. A different folder name is expected on another computer.

**Spoken script**

Let us read a small piece of code that tells us where we are running.

The word Path is a tool we import from a Python module called pathlib. It helps us work with file locations. The call Path dot cwd, with brackets, gives us the folder where Python is running right now. The letters cwd stand for current working directory, which is another name for the working folder.

Then dot name gives only the last folder in that location, as plain text. This depends on the computer and runtime. On your laptop the answer may be one folder name, and on a classmate's computer it will be another. That difference is expected. What matters is that the README states which folder the project should run from.

## Slide 29: Tell another person what the project needs

requirements.txt and versions

This text file lists required Python packages and their versions. Record the versions used in the working environment; test them with the supplied run instructions.

Data source, permission and seed

Name the data source and any licence or permission for reuse. Record random seeds used in modelling. A seed supports repeatability; it does not repair data leakage.

**Spoken script**

Two more items go in the handover.

The first is a file called requirements dot txt. It is a plain text file that lists the Python packages our project needs, with their versions. We record the versions from the environment where our project works. Then we test them by following our own run instructions.

The second item is information about the data and about randomness. We name where the data came from, and any licence or permission that allows us to reuse it. We also record the random seeds we used in modelling. A seed makes random choices repeat, so the split of data comes out the same each time. It helps repeatability. If the test data leaked into training, though, the seed leaves that problem in place.

## Slide 30: Recording the versions you used

Each line prints the version of one tool.
Copy the four results into requirements.txt and the README.
Write them as pandas==X.Y.Z, one tool on each line, with the numbers your own run printed.

Install later with: pip install -r requirements.txt

```python
import sys, pandas, numpy, sklearn
print(sys.version.split()[0])
print("pandas", pandas.__version__)
print("numpy", numpy.__version__)
print("scikit-learn", sklearn.__version__)
```

Output on the slide:

```text
(your versions print here)
```

**Spoken script**

A reader needs to know which versions of the tools you used, because a newer version can behave differently. This short cell asks Python for them. The first line imports the tools and the system module. The next lines print the Python version and the version of pandas, NumPy and scikit-learn.

Your own run prints the numbers. We copy them into a small text file called requirements dot txt, one tool on each line, written as the tool name, two equals signs and the version. Someone else can then install the same versions with one command, pip install dash r requirements dot txt, and mention the Python version in the README.

## Slide 31: A fresh start in Colab

BEFORE THE CHECK
Upload your data file to the Colab Files panel, or mount Drive.
Put the file where the README says, for example data/raw/engineering_data.csv.

THE CHECK
Choose Runtime, then Restart session, then Run all.
Disconnect and delete runtime wipes uploaded files, so you upload them again before the check.

**Spoken script**

In Colab, a fresh start has a few specific steps. Uploaded files live only as long as the runtime. So before the check, upload your data file to the Files panel, or mount Drive, and put it exactly where your README says it goes.

Then choose Runtime, Restart session, and Run all. A restart clears every variable from memory but keeps uploaded files. The other choice, Disconnect and delete runtime, wipes the uploaded files as well, so after that we upload them again before we run. If every cell runs from top to bottom with no error and the results match what we saved, the notebook passes our fresh-start check.

## Slide 32: Run checks and contribution evidence

Independent run check

Restart the session and follow your written instructions without relying on earlier variables. Record the first failure and its repair.

Contribution evidence

A record of each person’s work, tied to files, commits or explanations. It does not require making a private repository public.

**Spoken script**

Two final items for the handover.

An independent run check means we restart the session and follow our own written instructions, without relying on any variable we made earlier. We keep a record of the first place where it failed and how we repaired it. That record shows we really tested the instructions.

Contribution evidence is a record of what each person did. It points to files, commits or explanations. A commit is a saved step in the project history. For example, one member may say they wrote the cleaning function and can explain it. Making a private repository public is not required for this. We can show the evidence in the way the project brief allows.

## Slide 33: Useful feedback identifies an exact repair

01

Vague feedback: "It does not work."

02

Useful feedback: "Step 2 names data.csv, but the supplied file is readings.csv."

03

The repair is to make the instructions and actual filename agree.

**Spoken script**

When we test a classmate's project, how should we report problems?

Vague feedback says, it does not work. That tells the author nothing about where to look.

Useful feedback is exact. For example, Step 2 names data dot csv, but the supplied file is readings dot csv. Now the author knows the step, the problem, and what to change.

The repair is to make the instructions and the actual filename agree. Either we correct the text in the README, or we rename the file, and then we run the project again from the start. Good feedback names the failed step and the fix.

## Slide 34: Revision example and answer

Check: restart the notebook runtime and follow your README exactly, without using remembered variables.

If Step 2 names data.csv but the file is readings.csv, correct the filename in the instructions. Run again from the beginning and record the successful result.

**Spoken script**

Here is a short revision example for you to try alone, and then we check the answer.

The check is this. We restart the notebook runtime, then we follow our README exactly, without using any variable we remember from earlier.

Suppose Step 2 says to load data dot csv, but the file in the folder is called readings dot csv. The run fails at that step. The fix is to correct the filename in the instructions. Then we run again from the beginning, and when it works, we record the successful result. Notice that we start over each time, because a repair near the end is only proven when the whole run passes.

## Slide 35: Block 2 closes after today

No new weekly assignment.

The Block 2 pack, A10 and A11 for 40 marks, is due Thursday 10 December 2026, 23:59 Kampala time.
The Block 2 quiz covers Weeks 11, 12 and 13. It opens after today's class.
Next week is Practical Test 2. Rehearse saving and submitting your test notebook, and revise the published function interfaces.

**Spoken script**

There is no new assignment this week. Block 2 closes with two things.

The first is the Block 2 assignment pack, which is part A from Week 11 and part B from Week 12, forty marks in all, due Thursday 10 December at 23:59 Kampala time. The second is the Block 2 quiz, fifteen questions across Weeks 11, 12 and 13, which opens after today's class.

Next week is Practical Test 2. Rehearse saving your test notebook and submitting it, and revise the function interfaces. An interface is the function name, its inputs and what it returns, and the test expects them exactly as published.

## Slide 36: A reproducible handover

01

An absolute path from your own computer will usually fail elsewhere.

02

A relative path starts from the current working folder.

03

Record dependencies and actual versions, and fix randomness where appropriate; identical results across all machines are not guaranteed by a seed alone.

04

Captions should state a supported finding and its scope.

**Spoken script**

Let us gather what makes a handover reproducible, in four points.

One. An absolute path from our own computer, such as one that includes our username, will usually fail on someone else's machine.

Two. A relative path starts from the current working folder, so it travels with the project.

Three. We record the dependencies and the actual versions, and we fix randomness where appropriate by setting seeds. A seed alone does not guarantee identical results on every machine, so we describe our setup too.

Four. Our chart captions should state a finding that the evidence supports, and say how far it applies.

## Slide 37: A reproducible handover continued

Remove conflicting cell assignments and verify a fresh run before submission.

**Spoken script**

One last handover habit.

Before we submit, we remove conflicting cell assignments. That means we search the notebook for places where the same variable is given different values in different cells, because the final answer then depends on which cell was run last.

After that cleanup, we verify a fresh run. We restart the session, run everything from the top, and check that the results match what we report. Only then do we submit.

## Slide 38: Project preparation

01

Use the published machine learning project brief.

02

Build the evidence gradually in your project notebook.

03

Keep raw data, labelled charts, run instructions and individual contributions.

04

Published deadline: 18 Dec 2026, 11:00 Kampala

**Spoken script**

Now to our project preparation. There are four steps.

First, use the published machine learning project brief. It is the official statement of what we must deliver.

Second, build the evidence gradually in the project notebook. We add to it a little each week, so the work does not pile up at the end.

Third, keep the raw data, labelled charts, run instructions and each person's contribution.

Fourth, check the published deadline on the slide, and plan backward from it so the independent run check is finished with time to spare.

## Slide 39: Block 2 quiz: three forms, 15 questions

01

Week 11 form (5 questions)

Open the Week 11 quiz form

02

Week 12 form (5 questions)

Open the Week 12 quiz form

03

Week 13 form (5 questions)

Open the Week 13 quiz form

Opens after today's class. Each form stays open for 24 hours. Use your Student Registration Number and registered account.

**Spoken script**

The Block 2 quiz is three short forms, one for each week of the block, with five questions each. Together they are fifteen questions and fifteen marks.

The forms open after today's class, when the lecturer activates them, and each stays open for twenty-four hours. Open them one after the other and answer individually, using your Student Registration Number and your registered account.

This quiz replaces the three weekly quizzes of Weeks 11, 12 and 13. Like the assignment pack, it counts in full and is not dropped.

## Slide 40: Revision and submission checklist

Another learner can follow your README and reproduce the stated result.

Check that the required files are in place.

Point to your evidence. Save your work.

**Spoken script**

This is our individual exit check.

Explain it to yourself first. Another learner should be able to follow your README and reproduce the stated result. Ask whether that is true of your project today.

Then point to your evidence. Find the file, the chart or the run record that shows it. Save your work, and check which files are required for submission, so that what you submit is the file you intended.

If something is missing, note it now and fix it before you leave.

## Slide 41: Optional revision video

01

For revision after class.

02

CodeWithChris
GitHub Tutorial for Beginners (2025)

03

00:00–02:10, then 03:35–06:08 (4 min 43 sec total)

04

Listening question: Why keep history, and what is a repository?

Open explainer video

https://www.youtube.com/watch?v=v5gnvDUWqFM

**Spoken script**

This video is optional, and it is meant for revision after class.

It is a GitHub tutorial for beginners from CodeWithChris. Watch the parts shown on the slide, from the start to two minutes ten seconds, and then from three thirty-five to six oh eight. Together that is about four minutes forty-three seconds.

As you watch, keep this question in mind. Why do we keep history, and what is a repository? Try to answer it in your own words afterwards. The link is on the slide.
