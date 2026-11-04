"""Class 1 lab notebook: your first model. One notebook per cohort, same steps, the cohort's own data and units."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
from nb import Notebook  # noqa: E402
import common as C  # noqa: E402


def build(code):
    f = C.facts(code)
    unit, short, thing = f['unit'], f['short'], f['thing']
    nb = Notebook()
    nb.md(f'# Class 1 lab: your first model\n\n**{f["name"].replace("  |  ", ", ")}**  |  Week 8  |  KLAi at IUEA\n\n'
          f'In the lab you build three models that predict **{short}** (in **{unit}**) from two readings, and you compare them fairly.\n\n'
          '**How to use this notebook**\n\n'
          '1. Run the cells in order from the top. Press Shift and Enter to run a cell.\n'
          '2. Every step has the same rhythm: **PREDICT** what will happen, **RUN** the cell, **READ** the output, then **CHANGE** one thing and see what moves.\n'
          '3. Type your answers in the lines that start with `>`. Double-click a text cell to edit it.\n'
          '4. If you get an error, read the last line first. The slide called "Four errors you will meet" lists the common ones.\n\n'
          '**The words** (the real industry terms, also on the slides): a *feature* is an input column (also called an input variable or predictor). The *target variable* is the column we predict (when it is a class, such as yes or no, it is called a *label*; in Class 2 we make a yes or no label from the target). '
          'A *baseline model* is the simplest possible model: it predicts the mean of the training targets for every row, and every other model must beat it. '
          '*Prediction error* (also called the *residual*) is actual minus predicted: e = y - y-hat, where y is the actual target and y-hat is the prediction. *MAE* (mean absolute error) is the mean of the absolute errors. *RMSE* (root mean squared error) is the square root of the mean of the squared errors. '
          'The *training set* is the group of rows the model learns from. The *validation set* is held-out data: rows we keep back while the model trains, so that we can evaluate it fairly. '
          'A *missing value* is an empty cell (NaN in pandas), and *imputation* fills it. *Parameters* are the numbers a model learns (the intercept and coefficients). A *hyperparameter* is a setting we choose before training, such as `max_depth`.')

    nb.step(0, 'Open the data', 'First we load the file. Upload `engineering_data.csv` in the Files panel on the left of Colab (the folder icon) if you have not already.')
    nb.code('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n'
            '# read the file into a table. The raw table is never changed: we clean a copy.\n'
            'raw_data = pd.read_csv("engineering_data.csv")\n'
            'raw_data.head()')
    nb.md('The columns are: `record_id` (a number for each reading), `equipment_id` (which machine group, E1 to E6), `load_pct` (how hard it was working, in percent), '
          f'`ambient_c` (air temperature in degrees C) and `target` (the {short} in {unit}). The first two columns are labels. `load_pct` and `ambient_c` are our **features**. `target` is what we predict.')

    nb.step(1, 'Look before you clean', 'We always look at a table before we change it.')
    nb.predict('How many rows and columns does the table have? Is there any missing value?')
    nb.code('print("rows, columns:", raw_data.shape)\nprint()\nprint("missing values (NaN) in each column:")\nprint(raw_data.isna().sum())')
    nb.read('Which columns have missing values? A missing value in `target` is a different problem from a missing value in a feature column. Think about what we can do with a row that has no target value. Why is it more serious?')

    nb.step(2, 'Clean a copy: remove the rows we cannot trust', 'Three kinds of bad row: a repeated record_id, a row with a missing target value, and a load outside 0 to 100 percent.')
    nb.predict('How many rows will we lose in total? Use what the slides showed you.')
    nb.code('modelling_data = raw_data.drop_duplicates("record_id").copy()      # keep the first copy of each record_id\n'
            'print("after removing repeats:", len(modelling_data))\n\n'
            'has_target = modelling_data["target"].notna()                    # True where the target is recorded\n'
            'load_ok = modelling_data["load_pct"].between(0, 100)             # True where load is between 0 and 100\n'
            'modelling_data = modelling_data[has_target & load_ok].copy()     # keep rows that pass both checks\n'
            'print("rows left to model with:", len(modelling_data))')
    nb.read('Does the number of rows left match the number on the "Check your numbers" slide?')
    nb.change('Change `between(0, 100)` to `between(0, 90)` and run the cell again. Then change it back to 100 and run it once more. '
              'What does this tell you about how much one cleaning rule can change your data?')

    nb.step(3, 'Hold out data for a fair evaluation', 'Equipment groups E1 to E4 form the training set, E5 the validation set and E6 the test set. The validation set and the test set are held-out data: rows not used to fit the model. The test set stays untouched until the end of the course block.')
    nb.code('train_groups = ["E1", "E2", "E3", "E4"]\n\n'
            'training_data = modelling_data[modelling_data["equipment_id"].isin(train_groups)].copy()\n'
            'validation_data = modelling_data[modelling_data["equipment_id"] == "E5"].copy()\n'
            'test_data = modelling_data[modelling_data["equipment_id"] == "E6"].copy()   # we do not touch this today\n\n'
            'feature_columns = ["load_pct", "ambient_c"]\n'
            'print("training, validation, test rows:", len(training_data), len(validation_data), len(test_data))')
    nb.read('Why do we split by equipment group? What could go wrong if we picked random rows from every group?')
    nb.code('# the features (X) are a table. The target variable (y) is one column.\n'
            'X_train = training_data[feature_columns]\ny_train = training_data["target"]\n'
            'X_valid = validation_data[feature_columns]\ny_valid = validation_data["target"]\n\n'
            'print("X_train shape:", X_train.shape, "  y_train shape:", y_train.shape)\n'
            'print("missing values in X_train:", int(X_train.isna().sum().sum()), "  in X_valid:", int(X_valid.isna().sum().sum()))')
    nb.md('There is one missing value in a feature column, in `ambient_c` in the training set. A model cannot use a missing value, so in Step 5 **imputation** will fill it with the **median** (the middle value) of that column, using `SimpleImputer`. '
          'The median is found from the training set only, and the same number is used for any missing value in the validation set.')

    nb.step(4, 'Model 1: the baseline model', f'A baseline model is the simplest possible model. Here it is a mean predictor (`DummyRegressor`): it predicts the same number for every row, the mean of the training targets ({short}). Every other model must beat it.')
    nb.predict(f'About how far off, in {unit}, will the baseline model be on the validation set? Give a number.')
    nb.code('from sklearn.dummy import DummyRegressor\n'
            'from sklearn.metrics import mean_absolute_error, mean_squared_error\n\n'
            'baseline_model = DummyRegressor(strategy="mean")   # create the model\n'
            'baseline_model.fit(X_train, y_train)               # training (fitting): learn the mean of the training targets\n'
            'y_pred_baseline = baseline_model.predict(X_valid)   # inference: the same number for every validation row\n\n'
            'baseline_mae = mean_absolute_error(y_valid, y_pred_baseline)\n'
            f'print("The baseline model predicts", round(y_pred_baseline[0], 2), "{unit} for every row.")\n'
            f'print("Mean absolute error:", round(baseline_mae, 2), "{unit}")')
    nb.md('**Check by hand.** The prediction error (residual) of one row is `actual - predicted`, that is e = y - y-hat. The cell below shows five validation rows so that you can see the arithmetic behind the MAE: the MAE is the mean of the `absolute_error` column over all validation rows.')
    nb.code('check_rows = validation_data[["record_id", "target"]].head(5).copy()\n'
            'check_rows["predicted"] = y_pred_baseline[:5]\n'
            'check_rows["error"] = check_rows["target"] - check_rows["predicted"]\n'
            'check_rows["absolute_error"] = check_rows["error"].abs()\n'
            'check_rows.round(2)')
    nb.read('Pick one row. Check that `error = target - predicted`. Is the error positive when the baseline model predicted too low?')

    nb.step(5, 'Model 2: multiple linear regression', 'A linear regression model predicts the target as an intercept plus weighted features. With two features it is called multiple linear regression (with one feature it is simple linear regression). Training chooses the parameters that give the smallest mean squared error on the training set. '
            'The formula is y-hat = b0 + b1 x1 + b2 x2, where x1 is `load_pct`, x2 is `ambient_c`, b0 is the intercept (bias) and b1, b2 are the coefficients (weights). '
            'We chain the imputer and the model in a scikit-learn **pipeline**, which runs the steps in order.')
    nb.predict('Will multiple linear regression beat the baseline model? By a little or by a lot?')
    nb.code('from sklearn.impute import SimpleImputer\n'
            'from sklearn.pipeline import make_pipeline\n'
            'from sklearn.linear_model import LinearRegression\n\n'
            'linear_model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())\n'
            'linear_model.fit(X_train, y_train)            # training (fitting): learn the median, then b0, b1 and b2\n'
            'y_pred_linear = linear_model.predict(X_valid)    # inference: predictions for the validation set\n\n'
            'linear_mae = mean_absolute_error(y_valid, y_pred_linear)\n'
            'linear_rmse = mean_squared_error(y_valid, y_pred_linear) ** 0.5\n'
            f'print("Mean absolute error:", round(linear_mae, 2), "{unit}")\n'
            f'print("Root mean squared error:", round(linear_rmse, 2), "{unit}")')
    nb.code('# open the model and read the parameters it learned\n'
            'lin_reg = linear_model.named_steps["linearregression"]\n'
            'print("intercept:", round(lin_reg.intercept_, 3))\n'
            'print("coefficient b1 for load_pct:", round(lin_reg.coef_[0], 3))\n'
            'print("coefficient b2 for ambient_c:", round(lin_reg.coef_[1], 3))')
    nb.read(f'In plain words, what does the coefficient (weight) b1 for `load_pct` say about {short}? Complete this sentence and use the unit {unit}: "When load_pct goes up by 1 percent and ambient_c stays the same, the prediction goes up by ..."')
    nb.code('# check the formula by hand on the first validation row: b0 + b1 * load_pct + b2 * ambient_c\n'
            'first_row = validation_data.iloc[0]\n'
            'by_hand = lin_reg.intercept_ + lin_reg.coef_[0] * first_row["load_pct"] + lin_reg.coef_[1] * first_row["ambient_c"]\n'
            f'print("by hand:", round(by_hand, 2), "{unit}")\n'
            'print("model.predict:", round(y_pred_linear[0], 2))')
    nb.read('Are the two numbers the same? What does that tell you about what the model has learned (its parameters)?')
    nb.code('# plot the actual values against the predicted values. Points near the dashed line are accurate predictions (small prediction errors).\n'
            'plt.figure(figsize=(5, 4))\n'
            'plt.scatter(y_valid, y_pred_linear)\n'
            'low, high = y_valid.min(), y_valid.max()\n'
            'plt.plot([low, high], [low, high], linestyle="--")\n'
            f'plt.xlabel("actual {short} ({unit})")\nplt.ylabel("predicted ({unit})")\nplt.title("Multiple linear regression, validation set")\nplt.show()')
    nb.change('In Step 3 the features are `["load_pct", "ambient_c"]`. Make a new pipeline that uses only `["load_pct"]` and compare its MAE with the one above. '
              'Does the second feature help? This is simple linear regression (one feature) from the slides, and the model above is multiple linear regression.')
    nb.code('# your experiment: simple linear regression, one feature only (load_pct)\n'
            'simple_model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())\n'
            'simple_model.fit(training_data[["load_pct"]], y_train)\n'
            'simple_mae = mean_absolute_error(y_valid, simple_model.predict(validation_data[["load_pct"]]))\n'
            f'print("MAE of simple linear regression (load_pct only):", round(simple_mae, 2), "{unit}")')

    nb.step(6, 'Model 3: a decision tree', 'A decision tree asks a short list of yes or no questions about the features (internal nodes) and ends in leaf nodes that give the prediction. `max_depth=4` is a hyperparameter: a setting we choose before training. It allows at most four questions in a row. `random_state=17` makes the result repeatable.')
    nb.predict('Will the decision tree beat multiple linear regression? Give a reason.')
    nb.code('from sklearn.tree import DecisionTreeRegressor\n\n'
            'tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))\n'
            'tree_model.fit(X_train, y_train)\n'
            'y_pred_tree = tree_model.predict(X_valid)\n\n'
            'tree_mae = mean_absolute_error(y_valid, y_pred_tree)\n'
            'tree_rmse = mean_squared_error(y_valid, y_pred_tree) ** 0.5\n'
            f'print("Mean absolute error:", round(tree_mae, 2), "{unit}")\n'
            f'print("Root mean squared error:", round(tree_rmse, 2), "{unit}")')
    nb.change('Change `max_depth=4` to `max_depth=1`, then `2`, then `8`, running the cell each time and writing down the MAE. Put the depth back to 4 afterwards. '
              'Do not worry about the pattern yet: in Class 3 we explain what you are seeing (overfitting and underfitting).')

    nb.step(7, 'The model comparison table', 'All three models were trained on the same training set and evaluated on the same validation set. That is what makes the comparison fair.')
    nb.code('baseline_rmse = mean_squared_error(y_valid, y_pred_baseline) ** 0.5\n'
            '# MSE is the mean of the squared errors (unit squared). RMSE is its square root (the unit of the target).\n'
            'mse = [mean_squared_error(y_valid, p) for p in (y_pred_baseline, y_pred_linear, y_pred_tree)]\n'
            'results = pd.DataFrame({\n'
            '    "model": ["Baseline model (mean predictor)", "Multiple linear regression", "Decision tree, max_depth 4"],\n'
            '    "MAE": [baseline_mae, linear_mae, tree_mae],\n'
            '    "MSE": mse,\n'
            '    "RMSE": [baseline_rmse, linear_rmse, tree_rmse],\n'
            '}).round(2)\n'
            'print(results.to_string(index=False))')
    nb.code('plt.figure(figsize=(6, 3.5))\n'
            'plt.barh(results["model"], results["MAE"])\n'
            f'plt.xlabel("mean absolute error ({unit}), lower is better")\nplt.gca().invert_yaxis()\nplt.show()')
    nb.md('**Write your conclusion in two sentences.** Which model is best on the validation set? How much better is it than the baseline model? Use the unit in your answer.\n\n> My conclusion: ')
    n_va = len(f['va'])
    nb.md(f'**What this does not prove.** The data are synthetic teaching data. The validation set has only {n_va} rows. The test set (E6) has not been used. '
          'In Classes 3 and 4 we learn how to judge a model with more care.')

    nb.step(8, 'Save your work', 'Choose **Runtime, then Restart session and run all**. If every cell runs without an error, choose **File, then Save a copy in Drive**. '
            'Keep this notebook file safe. Class 2 uses a new notebook, and you reuse the cleaning steps from this one. This notebook is for learning. It is not the graded upload.')
    return nb


def CHECK(code, res, f):
    """The printed numbers must equal the reference values that are on the slides."""
    b = f['b']
    text = '\n'.join(o for _, o, _ in res)
    probs = []
    r = b['reg']
    L_ = b['line_load_only']
    lo_mae = float(abs(f['va'].target.to_numpy() - (L_['intercept'] + L_['slope'] * f['vaf'].load_pct.to_numpy())).mean())
    want = [f'rows left to model with: {b["n_clean"]}', f'training, validation, test rows: {b["n_tr"]} {b["n_va"]} {b["n_te"]}',
            f'Mean absolute error: {round(r["baseline"]["mae"], 2)}', f'Mean absolute error: {round(r["linear"]["mae"], 2)}', f'Mean absolute error: {round(r["tree"]["mae"], 2)}',
            f'Root mean squared error: {round(r["linear"]["rmse"], 2)}', f'Root mean squared error: {round(r["tree"]["rmse"], 2)}', f'intercept: {round(b["lin"]["intercept"], 3)}', f'coefficient b1 for load_pct: {round(b["lin"]["w_load"], 3)}',
            f'coefficient b2 for ambient_c: {round(b["lin"]["w_amb"], 3)}', f'by hand: {round(b["lin"]["intercept"] + b["lin"]["w_load"] * float(f["va"].load_pct.iloc[0]) + b["lin"]["w_amb"] * float(f["va"].ambient_c.iloc[0]), 2)}', f'rows, columns: ({len(f["raw"])}, 5)', f'MAE of simple linear regression (load_pct only): {round(lo_mae, 2)}']
    for w in want:
        if w not in text:
            probs.append(f'missing expected output: {w}')
    return probs
