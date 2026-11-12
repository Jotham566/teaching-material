"""Class 4 lab notebook: features and choosing a model. One notebook per cohort, same steps, the cohort's own data and units."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nb import Notebook  # noqa: E402
import common as C  # noqa: E402
import c4  # noqa: E402


def build(code):
    f = C.facts(code)
    unit, short, thing = f['unit'], f['short'], f['thing']
    nb = Notebook()
    nb.md(f'# Class 4 lab: features and choosing a model\n\n**{f["name"].replace("  |  ", ", ")}**  |  Week 11  |  KLAi at IUEA\n\n'
          f'In the lab you test a new feature with a feature ablation, meet two new models (ridge regression and k-nearest neighbours), build one model comparison table of five candidate models that predict **{short}** (in **{unit}**) and start your decision memo.\n\n'
          '**How to use this notebook**\n\n'
          '1. Run the cells in order from the top. Press Shift and Enter to run a cell.\n'
          '2. Every step has the same rhythm: **PREDICT** what will happen, **RUN** the cell, **READ** the output, then **CHANGE** one thing and see what moves.\n'
          '3. Type your answers in the lines that start with `>`. Double-click a text cell to edit it.\n'
          '4. If you get an error, read the last line first. The slide called "Four errors you will meet" lists the common ones.\n\n'
          '**The words** (also on the slides): *feature engineering* means building a new feature (an input variable) from features you already have. A *feature ablation* (also called an *ablation study*) is a fair test of one change: train the model with the feature and without it, on the same rows, and compare the two errors. '
          '*Ridge regression* is linear regression with *regularisation*: an L2 penalty on large weights (coefficients). *Alpha* is the regularisation strength. *k-NN* means k-nearest neighbours: to predict a new row, average the targets of the k training rows closest to it. k is a *hyperparameter*, a setting you choose before training. '
          '*Model selection* means choosing one model from several candidate models; here we use the client’s rule, as in the project. *Latency* (prediction time) is how long a trained model takes to give one prediction, in milliseconds. *Parsimony* means preferring the simpler model when it is good enough. '
          'A *decision memo* is a one-page note with your choice, your numbers and your limits. A related industry term is *model card*.\n\n'
          '**Two metrics.** *MAE* is the mean absolute error: the average size of the prediction error, in the same unit as the target. *RMSE* is the root mean squared error, which counts large errors more.')

    nb.step(1, 'Prepare the data again', 'This notebook stands alone. Upload `engineering_data.csv` in the Files panel of Colab if you have not already. The cell repeats the Class 1 preparation: it cleans a copy of the table and splits the rows by equipment group into a training set (E1 to E4), a validation set (E5) and a held-out test set (E6, the hold-out set).')
    nb.code('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n'
            'raw_df = pd.read_csv("engineering_data.csv")                  # the raw table is never changed\n'
            'clean_df = raw_df.drop_duplicates("record_id").copy()          # keep the first copy of each record_id\n'
            'has_target = clean_df["target"].notna()                        # True where the target variable is recorded\n'
            'load_ok = clean_df["load_pct"].between(0, 100)                 # True where load is between 0 and 100\n'
            'clean_df = clean_df[has_target & load_ok].copy()\n'
            'print("rows left to model with:", len(clean_df))\n\n'
            '# E1 to E4 form the training set, E5 the validation set, E6 the held-out test set\n'
            'train_df = clean_df[clean_df["equipment_id"].isin(["E1", "E2", "E3", "E4"])].copy()\n'
            'valid_df = clean_df[clean_df["equipment_id"] == "E5"].copy()\n'
            'test_df = clean_df[clean_df["equipment_id"] == "E6"].copy()   # held-out test set: opened once, in step 10, after we choose\n\n'
            'feature_columns = ["load_pct", "ambient_c"]\n'
            'X_train, y_train = train_df[feature_columns], train_df["target"]\n'
            'X_valid, y_valid = valid_df[feature_columns], valid_df["target"]\n'
            'print("training, validation, test rows:", len(train_df), len(valid_df), len(test_df))')
    nb.read('Do the numbers match the "Check your numbers" slide? If not, stop and ask before you go on.')

    nb.step(2, 'One loop, three models', f'A dictionary holds each model under its name, and a loop gives every model the same treatment. `with_imputer` is a helper, which means a small function that we write once and reuse. It builds a scikit-learn pipeline (a Pipeline chains preprocessing and a model): median imputation (`SimpleImputer`) fills each missing value (NaN, an empty cell) with the median of that column in the training set, and then the model is trained (fitted). '
            f'Every model is evaluated on the validation set with the same metric, the mean absolute error (MAE), in {unit}. The baseline model (`DummyRegressor`) always predicts the mean of the training target.')
    nb.predict('Which of the three will have the smallest error: the baseline model, linear regression or the decision tree?')
    nb.code('from sklearn.dummy import DummyRegressor\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.tree import DecisionTreeRegressor\n'
            'from sklearn.impute import SimpleImputer\nfrom sklearn.pipeline import make_pipeline\n'
            'from sklearn.metrics import mean_absolute_error, mean_squared_error\n\n'
            'def with_imputer(model):\n    # first fill missing values with the median of the training set (imputation), then train the model\n'
            '    return make_pipeline(SimpleImputer(strategy="median"), model)\n\n'
            'models = {\n    "Baseline model": with_imputer(DummyRegressor()),\n    "Linear regression": with_imputer(LinearRegression()),\n'
            '    "Decision tree, depth 4": with_imputer(DecisionTreeRegressor(max_depth=4, random_state=17)),   # same seed every time\n}\n\n'
            'rows = []\nfor name, model in models.items():\n    model.fit(X_train, y_train)          # training (fitting) the model\n    y_pred = model.predict(X_valid)      # inference: predictions for the validation set\n'
            '    mae = mean_absolute_error(y_valid, y_pred)\n    rmse = mean_squared_error(y_valid, y_pred) ** 0.5\n'
            '    rows.append([name, mae, rmse])\n'
            'results = pd.DataFrame(rows, columns=["model", "MAE", "RMSE"]).round(2)\n'
            'print(results.to_string(index=False))')
    nb.read('Do the three rows match the Class 1 model comparison table? Why does the loop keep the comparison fair?')

    nb.step(3, 'A new feature and a feature ablation', f'Idea from engineering sense: a {thing} working hard in hot air may need more than load and temperature explain separately. We build `load_x_ambient` (load_pct times ambient_c, an interaction feature, which is a product of two features) and also `load_squared` (load_pct times itself). '
            'A feature ablation (ablation study) then changes one thing at a time: each version of the linear regression model is trained on the same training set and scored on the same validation set.')
    nb.predict('Will the new feature lower the error by a lot, a little or not at all? Will removing `ambient_c` raise it by a lot or a little?')
    nb.code('# build each new feature on BOTH tables, with the same rule\n'
            'for table in (train_df, valid_df):\n'
            '    table["load_x_ambient"] = table["load_pct"] * table["ambient_c"]\n'
            '    table["load_squared"] = table["load_pct"] ** 2\n\n'
            'feature_sets = {\n    "Remove ambient_c (load only)": ["load_pct"],\n    "Two features (start)": ["load_pct", "ambient_c"],\n'
            '    "Add load_x_ambient": ["load_pct", "ambient_c", "load_x_ambient"],\n    "Add load_squared": ["load_pct", "ambient_c", "load_squared"],\n}\n\n'
            'for name, columns in feature_sets.items():\n    model = with_imputer(LinearRegression())\n    model.fit(train_df[columns], y_train)\n'
            '    mae = mean_absolute_error(y_valid, model.predict(valid_df[columns]))\n'
            f'    print(f"{{name}}: MAE {{mae:.2f}} {unit}")')
    nb.read('Which change moved the error a lot, and which hardly at all? Would you keep `load_x_ambient`? Give the reason in one sentence.')
    nb.md('**The learned parameters.** Each linear regression model is a formula: prediction = intercept (bias) + weight 1 times feature 1 + weight 2 times feature 2 (and weight 3 times feature 3 for the extended model). The weights are also called coefficients. In model A, one more unit of a feature adds its weight to the prediction, when the other feature stays fixed. In model B, `load_x_ambient` moves whenever `load_pct` moves, so the effect of one more percent of load is the weight for load_pct plus the weight for load_x_ambient times ambient_c. The next cell prints these numbers for model A (multiple linear regression on two features) and model B (plus the interaction feature `load_x_ambient`). They are the numbers on the formula slide.')
    nb.code('for name, columns in [("Model A, two features", ["load_pct", "ambient_c"]), ("Model B, plus load_x_ambient", ["load_pct", "ambient_c", "load_x_ambient"])]:\n'
            '    pipeline = with_imputer(LinearRegression())\n    pipeline.fit(train_df[columns], y_train)\n    linear_model = pipeline.steps[-1][1]        # the linear regression model itself, without the imputation step\n'
            '    weights = ", ".join(f"weight for {c} {w:.4f}" for c, w in zip(columns, linear_model.coef_))\n'
            '    print(f"{name}: intercept {linear_model.intercept_:.4f}, {weights}")')
    nb.read('Which weight is the smallest in model B? What does a tiny weight on `load_x_ambient` tell you about the new feature?')
    nb.change('Make your own feature, for example `ambient_squared`, on both tables and add it to `feature_sets`. Run the loop again. Did your idea help?')

    nb.step(4, 'One-hot encoding of a categorical feature', 'One-hot encoding turns a categorical feature (here equipment_id) into one column per category. In the training table, a row has a 1 in the column of its own group and a 0 in every other column, so each training row has exactly one 1. The validation group E5 is equipment the model never saw, so it gets a column of its own (`is_E5`) that the training table lacks. If we squeeze E5 into the four training columns, its row is all zeros. We only look at this here. We do not use equipment_id as a feature.')
    nb.code('one_hot_train = pd.get_dummies(train_df["equipment_id"], prefix="is").astype(int)\n'
            'print(pd.concat([train_df["equipment_id"], one_hot_train], axis=1).head(5).to_string(index=False))\n\n'
            'one_hot_valid = pd.get_dummies(valid_df["equipment_id"], prefix="is").astype(int)\n'
            'print()\nprint("columns the model learned from:", list(one_hot_train.columns))\n'
            'print("columns the validation group has:  ", list(one_hot_valid.columns))\n'
            'print()\nprint("E5 rows squeezed into the training columns (all zeros):")\n'
            'print(one_hot_valid.reindex(columns=one_hot_train.columns, fill_value=0).head(2).to_string(index=False))')
    nb.read(f'The validation group has a column (`is_E5`) that the training table does not, and E5 squeezed into the training columns is all zeros. What can a model say about a {thing} group it has never seen from four zeros? Why do we leave `equipment_id` out of the features?')

    nb.step(5, 'Scaling and ridge regression', 'Ridge regression adds an L2 penalty on large weights. This is regularisation, and alpha is the regularisation strength. The penalty depends on the size of the weights, which depends on the units of the features, so we standardise first: standardised value (z-score) = (value minus the training mean) divided by the training standard deviation. `StandardScaler` is the scikit-learn tool that does this: it learns the mean and standard deviation from the training set only, then applies them to any rows.')
    nb.predict('Linear regression on two features is not very flexible. Will a stronger penalty (a bigger alpha) help it?')
    nb.code('from sklearn.preprocessing import StandardScaler, PolynomialFeatures\nfrom sklearn.linear_model import Ridge\n\n'
            'X_train_imputed = SimpleImputer(strategy="median").fit_transform(X_train)   # missing values imputed with the training median\n'
            'scaler = StandardScaler().fit(X_train_imputed)\n'
            'print("training mean of load_pct:", round(scaler.mean_[0], 1), " standard deviation:", round(scaler.scale_[0], 1))\n\n'
            '# part A: ridge regression on two features, with a few values of alpha\n'
            'for alpha in [0.1, 1, 10]:\n    ridge_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=alpha))\n'
            '    ridge_model.fit(X_train, y_train)\n    mae = mean_absolute_error(y_valid, ridge_model.predict(X_valid))\n'
            f'    print(f"Ridge, two features, alpha {{alpha:g}}: MAE {{mae:.2f}} {unit}")')
    nb.read('Does a bigger alpha lower the error of the linear model? When does ridge regression help, and when does it not?')
    nb.predict('A sixth-degree curve of load_pct is very flexible. Which alpha will give the lowest validation error: no penalty, 1 or 100?')
    nb.code('# part B: a flexible curve (a sixth-degree polynomial of load_pct alone) with and without regularisation\n'
            'load_train, load_valid = train_df[["load_pct"]], valid_df[["load_pct"]]\n\n'
            'for name, last_step in [("degree 6, no penalty", LinearRegression()), ("degree 6, ridge alpha 1", Ridge(alpha=1)), ("degree 6, ridge alpha 100", Ridge(alpha=100))]:\n'
            '    curve_model = make_pipeline(PolynomialFeatures(degree=6, include_bias=False), StandardScaler(), last_step)\n'
            '    curve_model.fit(load_train, y_train)\n'
            '    train_mae = mean_absolute_error(y_train, curve_model.predict(load_train))\n'
            '    valid_mae = mean_absolute_error(y_valid, curve_model.predict(load_valid))\n'
            '    biggest = abs(curve_model.steps[-1][1].coef_).max()       # the largest weight (coefficient) the model uses\n'
            f'    print(f"{{name}}: training MAE {{train_mae:.2f}}, validation MAE {{valid_mae:.2f}} {unit}, biggest weight {{biggest:.0f}}")')
    nb.read('What happens to the biggest weight as the penalty grows? At which alpha is the validation error lowest? This curve uses load_pct alone, so it is a different model from the ridge regression on two features in part A. Compare these three rows only with each other.')
    nb.md('**The ridge regression loss.** Ridge regression makes this number small: loss = sum of squared errors + alpha times the sum of squared weights (the L2 penalty). The next cell works it out for linear regression on the two scaled features. Alpha 0 is ordinary linear regression.')
    nb.code('# part C: the two parts of the ridge regression loss, on the scaled training set\n'
            'X_train_scaled = scaler.transform(X_train_imputed)\n'
            'for alpha in [0, 0.1, 1, 10]:\n    ridge_fit = Ridge(alpha=alpha).fit(X_train_scaled, y_train)\n'
            '    residuals = np.asarray(y_train) - ridge_fit.predict(X_train_scaled)     # residual = actual minus predicted\n    squared_errors = (residuals ** 2).sum()\n    squared_weights = (ridge_fit.coef_ ** 2).sum()\n'
            '    print(f"alpha {alpha:g}: weights {ridge_fit.coef_[0]:.2f} {ridge_fit.coef_[1]:.2f}, sum of squared errors {squared_errors:.1f}, alpha x sum of squared weights {alpha * squared_weights:.1f}, loss {squared_errors + alpha * squared_weights:.1f}")')
    nb.read('As alpha grows, what happens to the two weights, to the sum of squared errors and to the penalty part? Check one row by hand: do the two parts add up to the loss?')
    nb.change('In part A, add 1000 to the list of alphas and run it again. How does the validation error change as alpha grows? In part B, at which alpha is the validation error lowest?')

    nb.step(6, 'k-nearest neighbours (k-NN)', 'k-NN means k-nearest neighbours. To predict a new row, the model finds the k training rows closest to it, measured on the scaled features, and averages their targets. The distance between two rows is d = square root of ((gap in scaled load)^2 + (gap in scaled ambient)^2): square each gap, add the two, then take the square root (Euclidean distance). k is a hyperparameter: a setting you choose before training.')
    nb.predict('Which k will give the smallest error: 1, 3 or 20?')
    nb.code('from sklearn.neighbors import KNeighborsRegressor\n\n'
            'for k in [1, 3, 20]:\n    knn_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), KNeighborsRegressor(n_neighbors=k))\n'
            '    knn_model.fit(X_train, y_train)\n    mae = mean_absolute_error(y_valid, knn_model.predict(X_valid))\n'
            f'    print(f"k = {{k}}: MAE {{mae:.2f}} {unit}")')
    nb.read('Why is k = 20 worse than k = 3? Why is k = 1 risky?')
    nb.code('# open the box: which three training rows are closest to the first validation row?\n'
            'X_valid_scaled = scaler.transform(SimpleImputer(strategy="median").fit(X_train).transform(X_valid))\n'
            'knn_3 = KNeighborsRegressor(n_neighbors=3).fit(X_train_scaled, y_train)\n'
            'distances, positions = knn_3.kneighbors(X_valid_scaled[:1])\n'
            'neighbours = train_df.iloc[positions[0]]\n'
            'print("new row: record", valid_df["record_id"].iloc[0], " actual", y_valid.iloc[0])\n'
            'print(neighbours[["record_id", "load_pct", "ambient_c", "target"]].to_string(index=False))\n'
            'print("distances to the 3 neighbours:", ", ".join(f"{d:.3f}" for d in distances[0]))\n'
            f'print(f"average of the 3 targets: {{neighbours[\'target\'].mean():.1f}} {unit}")')
    nb.change('Change `n_neighbors=3` to 5 in the last cell and run it again. Write down the three or five record numbers you see.')

    nb.step(7, 'The model comparison table', 'Five candidate models, one loop: this is model comparison with the same protocol. Same training set, same validation set, same metrics, same seed. The cross-validated columns use GroupKFold cross-validation: each of E1 to E4 is held out once as a whole equipment group (scikit-learn chooses the order), and the model learns from the other three groups, so each fold plays equipment the model has never met. '
            '`CV mean` is the mean of the four fold MAEs. `CV SD` is their sample standard deviation: `cv_scores.std(ddof=1)` divides by k minus 1 = 3, as the project does. `CV lowest` and `CV highest` are the smallest and largest fold MAE.')
    nb.predict('Which model will have the lowest cross-validated error? Will the same model win on the validation set?')
    nb.code('from sklearn.model_selection import GroupKFold, cross_val_score\n\n'
            'models["Ridge regression, alpha 1"] = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), Ridge(alpha=1))\n'
            'models["k-NN, k = 3"] = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), KNeighborsRegressor(n_neighbors=3))\n\n'
            'groups = train_df["equipment_id"]\ncv = GroupKFold(n_splits=4)\n\n'
            'rows = []\nfor name, model in models.items():\n    model.fit(X_train, y_train)\n    y_pred = model.predict(X_valid)\n'
            '    cv_scores = -cross_val_score(model, X_train, y_train, cv=cv, groups=groups, scoring="neg_mean_absolute_error")\n'
            '    mae = mean_absolute_error(y_valid, y_pred)\n    rmse = mean_squared_error(y_valid, y_pred) ** 0.5\n'
            '    rows.append([name, mae, rmse, cv_scores.mean(), cv_scores.std(ddof=1), cv_scores.min(), cv_scores.max()])   # ddof=1: the sample standard deviation\n'
            'results = pd.DataFrame(rows, columns=["model", "valid MAE", "valid RMSE", "CV mean", "CV SD", "CV lowest", "CV highest"]).round(2)\n'
            'print(results.to_string(index=False))')
    nb.read('Which model has the lowest validation MAE? Which has the lowest CV mean? We do not choose yet: step 8 applies the client’s rule.')
    nb.code('plt.figure(figsize=(6.5, 3.8))\nplt.barh(results["model"], results["CV mean"])\n'
            f'plt.xlabel("cross-validated mean absolute error ({unit}), lower is better")\nplt.gca().invert_yaxis()\nplt.show()')
    nb.code('print("The test set has", len(test_df), "rows. We have not used it.")')

    mx = c4.MAX_MAE[code]
    nb.step(8, 'Choose a model by the client’s rule, with a function on records', 'The project gives you rows as **records**: each row is a dictionary, and a table is a list of dictionaries. Its functions take records and return lists. This step rehearses that form. '
            '`predict_records` wraps a pipeline in a function: it trains on a list of training records and returns one prediction per new record. A *list comprehension* builds a new list in one line. `sorted(..., key=lambda c: ...)` sorts records by the values the small `lambda` function gives. '
            f'The rule, as in the project: keep the models whose validation MAE is at most the client’s limit ({mx:.1f} {unit}) **and** whose latency (prediction time) is at most 50 ms; choose the lowest validation MAE; break a tie by the smaller latency, then by the name. The limits and latencies are invented teaching numbers. The test set never takes part.')
    nb.predict('Which model has the lowest validation MAE of all five? Will it pass both limits?')
    nb.code(f'MAX_MAE = {mx}      # the client accepts a validation MAE of at most this many {unit} (invented teaching number)\n'
            'MAX_MS = 50         # and a prediction time of at most 50 milliseconds (invented teaching number)\n'
            'LATENCY_MS = {"Baseline model": 1, "Linear regression": 3, "Decision tree, depth 4": 30,\n              "Ridge regression, alpha 1": 3, "k-NN, k = 3": 60}   # invented teaching numbers; k-NN compares each new row with every training row\n\n'
            'record_columns = ["record_id", "equipment_id", "load_pct", "ambient_c", "target"]\n'
            'train_records = train_df[record_columns].to_dict("records")    # a list of dictionaries, one per row\n'
            'valid_records = valid_df[record_columns].to_dict("records")\n'
            'print("first training record:", train_records[0])\n\n'
            'def predict_records(model, training_records, new_records):\n'
            '    """Train the pipeline on a list of records and return one prediction per new record, in order."""\n'
            '    table = pd.DataFrame(training_records)\n'
            '    new_table = pd.DataFrame(new_records)\n'
            '    model.fit(table[feature_columns], table["target"])\n'
            '    return model.predict(new_table[feature_columns]).tolist()\n\n'
            'valid_features = [{key: value for key, value in r.items() if key != "target"} for r in valid_records]   # the new rows have no target\n'
            'valid_actual = [r["target"] for r in valid_records]\n\n'
            'candidates = []\nfor name, model in models.items():\n'
            '    predictions = predict_records(model, train_records, valid_features)\n'
            '    candidates.append({"name": name, "validation_mae": mean_absolute_error(valid_actual, predictions), "latency_ms": LATENCY_MS[name]})\n\n'
            'kept = [c for c in candidates if c["validation_mae"] <= MAX_MAE and c["latency_ms"] <= MAX_MS]\n'
            'ranked = sorted(kept, key=lambda c: (c["validation_mae"], c["latency_ms"], c["name"]))\n'
            'for c in ranked:\n'
            f'    print(f"kept: {{c[\'name\']}}, MAE {{c[\'validation_mae\']:.2f}} {unit}, latency {{c[\'latency_ms\']}} ms")\n'
            'chosen_model = ranked[0]["name"] if ranked else None\n'
            'print("Chosen model:", chosen_model)')
    nb.read('Which models were removed by the error limit, and which by the latency limit? Why does the rule not use the cross-validated columns or the test set?')
    nb.change('Set `MAX_MS = 100` and run the cell again. Which model is chosen now, and why?')

    lim = f['b']['limit']
    nb.step(9, 'Choose the warning threshold by cost (recall Class 2)', f'The project asks a second question: which rows should raise a warning? A row is a warning (1) when its target is at or above {lim:g} {unit}. A logistic regression pipeline gives each validation row a probability, and the decision threshold turns it into 0 or 1. '
            'A missed warning (a false negative, FN) costs 5 and a false alarm (a false positive, FP) costs 1. These are invented teaching costs, the same as in the project: cost = 5 x FN + 1 x FP. We try thresholds 0.3, 0.5 and 0.7 and keep the lowest cost; if two tie, the higher threshold.')
    nb.predict('A lower threshold raises more warnings. Will it lower the cost or raise it?')
    nb.code('from sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import confusion_matrix, recall_score, precision_score\n\n'
            f'LIMIT = {lim}                          # a row is a warning (1) at or above this many {unit}\n'
            'MISSED_COST, FALSE_ALARM_COST = 5, 1   # invented teaching costs\n\n'
            'warning_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))\n'
            'warning_model.fit(X_train, (y_train >= LIMIT).astype(int))\n'
            'warning_actual = (y_valid >= LIMIT).astype(int)\n'
            'probability = warning_model.predict_proba(X_valid)[:, 1]     # column 1: the probability of a warning\n\n'
            'cost_table = []\nfor threshold in [0.3, 0.5, 0.7]:\n'
            '    predicted = [1 if p >= threshold else 0 for p in probability]   # a list comprehension\n'
            '    tn, fp, fn, tp = confusion_matrix(warning_actual, predicted).ravel()\n'
            '    cost = MISSED_COST * fn + FALSE_ALARM_COST * fp\n'
            '    cost_table.append({"threshold": threshold, "tp": int(tp), "fp": int(fp), "fn": int(fn), "tn": int(tn), "cost": int(cost)})\n'
            '    print(f"threshold {threshold}: TP {tp}, FP {fp}, FN {fn}, TN {tn}, cost {cost}")\n\n'
            'chosen_threshold = sorted(cost_table, key=lambda row: (row["cost"], -row["threshold"]))[0]["threshold"]   # lowest cost; a tie goes to the higher threshold\n'
            'print("Chosen threshold:", chosen_threshold)')
    nb.read('Check one cost by hand: 5 x FN + 1 x FP. Why does the minus sign in the sort key give the higher threshold when two costs tie?')

    nb.step(10, 'After the choice: five-group cross-validation, then open the test set once', 'Now the model and the threshold are chosen, the validation group E5 is no longer needed for choosing, so it can join the cross-validation. As in project Task 5, part A holds out each of E1 to E5 in turn, trains linear regression on the other four groups (rows with no missing value, so no imputation is needed) and reports the mean and the sample standard deviation of the five fold MAEs (`np.std(folds, ddof=1)`, which divides by 5 minus 1 = 4). '
            'Part B opens the held-out test set **once**, as in project Task 8: the chosen model is refitted on all development rows (training plus validation, E1 to E5) and scored on E6, and the chosen threshold is tested at the same time. The refit is allowed because the choice is already fixed and E6 is still unseen. Run part B one time only, and never change your choice after it.')
    nb.predict('Will the five-fold mean be close to the four-fold mean of step 7? Will the test MAE be larger or smaller than the validation MAE?')
    nb.code('# part A: group cross-validation over all five development groups, E1 to E5\n'
            'development_df = pd.concat([train_df, valid_df])                    # E1 to E5\n'
            'complete_df = development_df[development_df["ambient_c"].notna()]   # rows with no missing value\n'
            'folds = []\nfor group in ["E1", "E2", "E3", "E4", "E5"]:\n'
            '    fold_train = complete_df[complete_df["equipment_id"] != group]\n'
            '    fold_test = complete_df[complete_df["equipment_id"] == group]\n'
            '    fold_model = LinearRegression().fit(fold_train[feature_columns], fold_train["target"])\n'
            '    fold_mae = mean_absolute_error(fold_test["target"], fold_model.predict(fold_test[feature_columns]))\n'
            '    folds.append(fold_mae)\n'
            f'    print(f"held out {{group}}: {{len(fold_test)}} rows, MAE {{fold_mae:.2f}} {unit}")\n'
            f'print(f"five-group CV: mean {{np.mean(folds):.2f}}, sample standard deviation {{np.std(folds, ddof=1):.2f}} {unit}")')
    nb.code('# part B: open the test set ONCE, with the chosen model and the chosen threshold\n'
            'final_model = models[chosen_model]\n'
            'final_model.fit(development_df[feature_columns], development_df["target"])            # refit on E1 to E5\n'
            'test_mae = mean_absolute_error(test_df["target"], final_model.predict(test_df[feature_columns]))\n'
            'warning_model.fit(development_df[feature_columns], (development_df["target"] >= LIMIT).astype(int))\n'
            'test_probability = warning_model.predict_proba(test_df[feature_columns])[:, 1]\n'
            'test_warning = [1 if p >= chosen_threshold else 0 for p in test_probability]\n'
            'test_actual = (test_df["target"] >= LIMIT).astype(int)\n'
            f'print(f"Test set opened once: {{len(test_df)}} rows, {{chosen_model}}, MAE {{test_mae:.2f}} {unit}")\n'
            'print(f"Warnings at threshold {chosen_threshold}: recall {recall_score(test_actual, test_warning, zero_division=0):.2f}, precision {precision_score(test_actual, test_warning, zero_division=0):.2f}")')
    nb.read('Write the test MAE and the warning recall in your memo, whatever they are. Why would it be unfair to change your model now?')

    nb.step(11, 'Your decision memo', 'Fill in each sentence in your own words, with numbers from your results and their unit. Double-click the cell to edit it. One page is enough. In industry a related document is called a model card.')
    nb.md(f'**Decision memo: predicting {short}**\n\n'
          f'1. **Question.** We wanted to know whether we can predict ... on a new {thing}, and which rows should raise a warning.\n\n'
          '2. **Data.** We used ... training rows and ... validation rows. The data are ... \n\n'
          '3. **Models tried.** We tried ... \n\n'
          f'4. **Result.** By the client’s rule (MAE at most {mx:.1f} {unit}, latency at most 50 ms) we chose ..., with a validation MAE of ... {unit}. The baseline model had ... {unit}. The five-group cross-validated MAE was ... {unit}. On the test set, opened once, the MAE was ... {unit}.\n\n'
          '5. **Limits.** The numbers cannot tell us ... Four limits are ... \n\n'
          '6. **Recommendation.** I recommend ... with a warning threshold of ..., because ... \n\n'
          '7. **Next step.** Before anyone relies on it, we should ... ')

    nb.step(12, 'Save your work', 'Choose **Runtime, then Restart session and run all**. If every cell runs without an error, choose **File, then Save a copy in Drive**. Keep the notebook and your memo: the project uses these steps. The Engineering ML project is an individual, timed, auto-graded 3-hour sitting in Week 12 (proposed, lecturer to confirm), and a practice version, the rehearsal, is released right after Class 4.')
    return nb


def CHECK(code, res, f):
    """The printed numbers must equal the reference values that are on the slides."""
    import c4
    k = c4.compute(code)
    b = f['b']
    text = '\n'.join(o for _, o, _ in res)
    flat = ' '.join(text.split())
    probs = []
    u = f['unit']
    cand = {d['name']: d for d in k['cand']}
    want = [f'rows left to model with: {b["n_clean"]}', f'training, validation, test rows: {b["n_tr"]} {b["n_va"]} {b["n_te"]}']
    for n in ('Baseline model', 'Linear regression', 'Decision tree, depth 4'):
        want.append(f'{n} {round(cand[n]["mae"], 2):.2f} {round(cand[n]["rmse"], 2):.2f}')
    a = k['abl']
    for name, key in (('Remove ambient_c (load only)', 'load_only'), ('Two features (start)', 'base'), ('Add load_x_ambient', 'int'), ('Add load_squared', 'sq')):
        want.append(f'{name}: MAE {a[key]["mae"]:.2f} {u}')
    want += [f'training mean of load_pct: {k["scaler"]["mu"][0]:.1f}  standard deviation: {k["scaler"]["sd"][0]:.1f}'.replace('  ', ' ')]
    for al, key in ((0.1, 0.1), (1, 1.0), (10, 10.0)):
        want.append(f'Ridge, two features, alpha {al:g}: MAE {k["ridge2"][key]:.2f} {u}')
    for name, row in zip(('degree 6, no penalty', 'degree 6, ridge alpha 1', 'degree 6, ridge alpha 100'), k['ridge_poly']):
        want.append(f'{name}: training MAE {row["train"]:.2f}, validation MAE {row["valid"]:.2f} {u}, biggest weight {row["coef"]:.0f}')
    ln = k['lines']
    want.append(f'Model A, two features: intercept {ln["a"]["b0"]:.4f}, weight for load_pct {ln["a"]["w"][0]:.4f}, weight for ambient_c {ln["a"]["w"][1]:.4f}')
    want.append(f'Model B, plus load_x_ambient: intercept {ln["b"]["b0"]:.4f}, weight for load_pct {ln["b"]["w"][0]:.4f}, weight for ambient_c {ln["b"]["w"][1]:.4f}, weight for load_x_ambient {ln["b"]["w"][2]:.4f}')
    for d in k['ridge_tab']:
        want.append(f'alpha {d["alpha"]:g}: weights {d["w"][0]:.2f} {d["w"][1]:.2f}, sum of squared errors {d["sse"]:.1f}, alpha x sum of squared weights {d["pen"]:.1f}, loss {d["loss"]:.1f}')
    want.append('distances to the 3 neighbours: ' + ', '.join(f'{d["d"]:.3f}' for d in k['knn_tab'][:3]))
    for kk in (1, 3, 20):
        want.append(f'k = {kk}: MAE {k["knn"][kk]:.2f} {u}')
    ex = k['knn_ex']
    want.append(f'new row: record {ex["query_row"]} actual {ex["actual"]:g}')
    want.append(f'average of the 3 targets: {ex["prediction"]:.1f} {u}')
    for rid in ex['neighbours']:
        want.append(str(rid))
    for n in c4.MODEL_NAMES:
        d = cand[n]
        want.append(' '.join([n] + [f'{round(v, 2):.2f}' for v in (d['mae'], d['rmse'], d['cv_mean'], d['cv_sd'], d['cv_min'], d['cv_max'])]))
    for n in k['rule']['kept']:
        want.append(f'kept: {n}, MAE {cand[n]["mae"]:.2f} {u}, latency {cand[n]["latency"]} ms')
    want.append(f'Chosen model: {k["rule"]["chosen"]}')
    for t in k['cost_tab']:
        want.append(f'threshold {t["th"]:g}: TP {t["tp"]}, FP {t["fp"]}, FN {t["fn"]}, TN {t["tn"]}, cost {t["cost"]}')
    want.append(f'Chosen threshold: {k["threshold"]["th"]:g}')
    for d in k['cv5']['folds']:
        want.append(f'held out {d["group"]}: {d["n"]} rows, MAE {d["mae"]:.2f} {u}')
    want.append(f'five-group CV: mean {k["cv5"]["mean"]:.2f}, sample standard deviation {k["cv5"]["sd"]:.2f} {u}')
    t = k['test']
    want.append(f'Test set opened once: {t["n"]} rows, {k["rule"]["chosen"]}, MAE {t["mae"]:.2f} {u}')
    want.append(f'Warnings at threshold {k["threshold"]["th"]:g}: recall {t["recall"]:.2f}, precision {t["precision"]:.2f}')
    for w in want:
        if w not in flat:
            probs.append(f'missing expected output: {w}')
    return probs
