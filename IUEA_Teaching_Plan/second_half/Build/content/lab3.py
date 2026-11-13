"""Class 3 lab notebook: can I trust this model? Depth curve, K-fold and group K-fold, three leaks, seeds and a run record."""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'kit'))
from nb import Notebook  # noqa: E402
import common as C  # noqa: E402
import c3  # noqa: E402


def build(code):
    f = C.facts(code)
    unit, short, thing = f['unit'], f['short'], f['thing']
    N = c3.refs(f)
    d2 = lambda v: f'{v:.2f}'
    nb = Notebook()
    nb.md(f'# Class 3 lab: can I trust this model?\n\n**{f["name"].replace("  |  ", ", ")}**  |  Week 10  |  KLAi at IUEA\n\n'
          f'Today you test how far you can trust a model that predicts **{short}** (in **{unit}**): you watch a decision tree overfit, score it with cross-validation, plant three kinds of data leakage on purpose, fix the random seed, and practise the records form that the project uses.\n\n'
          '**How to use this notebook**\n\n'
          '1. Run the cells in order from the top. Press Shift and Enter to run a cell.\n'
          '2. Every step has the same rhythm: **PREDICT** what will happen, **RUN** the cell, **READ** the output, then **CHANGE** one thing and see what moves.\n'
          '3. Type your answers in the lines that start with `>`. Double-click a text cell to edit it.\n'
          '4. If you get an error, read the last line first. The slide called "Four problems you will meet" lists the common ones.\n\n'
          '**The words** (also on the slides): *overfitting* means the model fits the noise in the training set, so it does well there and worse on new rows; *underfitting* means it is too simple to learn the pattern. The *bias-variance trade-off* is the balance between the two: a too-simple model has high bias, a too-flexible model has high variance. '
          '*Cross-validation* scores a model K times. The rows are cut into K parts called *folds*, and each fold takes one turn as the *validation fold* (also called the held-out fold; it is not the sealed test set E6). '
          'The *generalisation gap* is the validation error minus the training error. *Data leakage* is information from outside the training set reaching the model. A *random seed* (random_state in scikit-learn) makes a random choice repeat exactly. '
          'An *imputer* fills missing values (we use the median of the column). A *scaler* (StandardScaler) rescales columns to a common scale. Both learn numbers from the rows, so they must be fitted on the training set only.\n\n'
          'The test set (group E6) stays sealed today. Nothing in this notebook uses it. It is opened once, at the very end, after the model and any threshold are chosen: the chosen model is refitted on E1 to E5 and scored once on E6. Class 4 shows that step.')

    nb.step(1, 'Prepare the data again', 'Same cleaning and the same split as Class 1, in a few lines. Upload `engineering_data.csv` in the Files panel if you have not already.')
    nb.code('import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\n'
            'raw_data = pd.read_csv("engineering_data.csv")\n'
            'modelling_data = raw_data.drop_duplicates("record_id").copy()          # keep the first copy of each record_id\n'
            'has_target = modelling_data["target"].notna()                          # a row needs a target\n'
            'load_ok = modelling_data["load_pct"].between(0, 100)                   # load must be 0 to 100 percent\n'
            'modelling_data = modelling_data[has_target & load_ok].copy()\n'
            'print("rows left to model with:", len(modelling_data))\n\n'
            '# split by equipment group, as in Class 1\n'
            'training_data = modelling_data[modelling_data["equipment_id"].isin(["E1", "E2", "E3", "E4"])].copy()\n'
            'validation_data = modelling_data[modelling_data["equipment_id"] == "E5"].copy()\n'
            'test_data = modelling_data[modelling_data["equipment_id"] == "E6"].copy()      # sealed: we never use it today\n'
            'print("training, validation, test rows:", len(training_data), len(validation_data), len(test_data))\n\n'
            'feature_columns = ["load_pct", "ambient_c"]\n'
            'X_train = training_data[feature_columns]\ny_train = training_data["target"]\n'
            'X_valid = validation_data[feature_columns]\ny_valid = validation_data["target"]\n'
            'groups = training_data["equipment_id"]        # which equipment group each training row belongs to')
    nb.read('Do the row counts match the "Check your numbers" slide? If not, stop and find the cell that went wrong.')

    nb.step(2, 'Underfitting, a good fit and overfitting: the validation curve', 'We train decision trees with max_depth 1 to 10 (max_depth is a hyperparameter: a setting chosen before training) and compare the error on the training set with the error on the validation set, rows the trees have never seen. Plotting both errors against max_depth gives a validation curve.')
    nb.predict('As the depth grows from 1 to 10, what will happen to the training error? And to the validation error?')
    nb.code('from sklearn.impute import SimpleImputer\n'
            'from sklearn.pipeline import make_pipeline\n'
            'from sklearn.tree import DecisionTreeRegressor\n'
            'from sklearn.metrics import mean_absolute_error\n\n'
            'depths = list(range(1, 11))\n'
            'train_maes = []\n'
            'valid_maes = []\n'
            'for depth in depths:\n'
            '    tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=depth, random_state=17))\n'
            '    tree_model.fit(X_train, y_train)                                      # training the model\n'
            '    train_mae = mean_absolute_error(y_train, tree_model.predict(X_train))     # training set\n'
            '    valid_mae = mean_absolute_error(y_valid, tree_model.predict(X_valid))     # validation set\n'
            '    train_maes.append(train_mae)\n'
            '    valid_maes.append(valid_mae)\n'
            '    print(f"depth {depth:2d}  training {train_mae:.2f}  validation {valid_mae:.2f}  generalisation gap {valid_mae - train_mae:.2f}")')
    nb.read('Where does the training error reach zero? Where does the validation error stop improving? How large is the generalisation gap at depth 10? Which depths look like underfitting and which like overfitting?')
    nb.md('**Choose max_depth with the validation set only.** The validation set has only a few rows, so its scores are noisy. Our rule is model selection by parsimony (prefer the simpler model when scores are close): find the lowest validation error, accept any depth within a tolerance of 5 percent of it, and take the simplest (smallest) depth among them. This is a common practical rule, not a law, and it is similar in spirit to the one-standard-error rule.')
    nb.code('lowest = min(valid_maes)\n'
            'within_tolerance = [d for d, v in zip(depths, valid_maes) if v <= lowest * 1.05]   # depths within 5 percent of the lowest\n'
            'best_depth = min(within_tolerance)                                                  # the simplest of them\n'
            f'print(f"lowest validation MAE: {{lowest:.2f}} {unit}")\n'
            'print("depths within the tolerance:", within_tolerance)\n'
            'print("chosen depth:", best_depth)\n'
            'print(f"limit (lowest x 1.05): {lowest * 1.05:.3f}")\n'
            'for d, v in zip(depths, valid_maes):                                                # three decimals, so a near miss shows\n'
            '    print(f"depth {d:2d}: validation {v:.3f}", "passes" if v <= lowest * 1.05 else "fails")\n\n'
            'plt.figure(figsize=(6, 3.8))\n'
            'plt.plot(depths, train_maes, marker="o", label="training")\n'
            'plt.plot(depths, valid_maes, marker="o", label="validation")\n'
            'plt.axvline(best_depth, linestyle="--")\n'
            f'plt.xlabel("max_depth")\nplt.ylabel("MAE ({unit})")\nplt.legend()\nplt.title("Validation curve: training and validation error")\nplt.show()')
    nb.read('Is the chosen depth the one with the very lowest validation error? Why did we accept the tolerance? Look at the training error at the chosen depth: is this tree also overfitting its training rows? Did we use the test group E6 anywhere?')
    nb.code('from sklearn.linear_model import LinearRegression\n\n'
            'linear_model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())\n'
            'linear_model.fit(X_train, y_train)\n'
            f'linear_mae = mean_absolute_error(y_valid, linear_model.predict(X_valid))\n'
            f'print(f"Linear regression, validation MAE: {{linear_mae:.2f}} {unit}")')
    nb.read('Compare the linear regression model from Class 1 with every tree in the table above. What does that say about the shape of this data?')
    nb.md(f'**CHECK.** You should see: validation MAE {d2(N["curve"][0][2])} at depth 1 and {d2(N["curve"][9][2])} at depth 10, depths within the tolerance {N["tie"]["passing"]}, chosen depth {N["best"]}, linear regression {d2(N["line_mae"])} {unit}.')
    mult = '1.10' if len(N['tie']['passing']) == 1 else '1.00'
    nb.change(f'In both places, change `lowest * 1.05` to `lowest * {mult}` and run the cell again. Which depth is chosen now? Then put it back to 1.05. Remember the depths 1, 2 and 8 you tried at the end of Class 1: this curve is what you were seeing.')

    nb.step(3, 'One split can be lucky: K-fold and GroupKFold cross-validation', 'We score the max_depth 4 tree from Class 1 on the training rows only. K-fold cross-validation cuts the rows into folds. Each fold takes one turn as the validation fold (held-out fold) while the tree is trained on the other folds. We do it with a loop first, then with the one-line shortcut cross_val_score. Each score is a MAE, and we report their mean and standard deviation.')
    nb.predict('Five fold scores will not all be equal. Will they differ by a little or by a lot? Will their mean be close to the single validation score of the depth-4 tree?')
    nb.code('from sklearn.model_selection import KFold, GroupKFold, cross_val_score\n\n'
            'kfold = KFold(n_splits=5)          # cut the 58 training rows into 5 folds, in order\n'
            'cv_scores = []\n'
            'for number, (train_idx, valid_idx) in enumerate(kfold.split(X_train), start=1):\n'
            '    tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))\n'
            '    tree_model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])           # the imputer is also fitted on the training folds only\n'
            '    y_pred = tree_model.predict(X_train.iloc[valid_idx])\n'
            '    mae = mean_absolute_error(y_train.iloc[valid_idx], y_pred)\n'
            '    cv_scores.append(mae)\n'
            '    print(f"fold {number}: train on {len(train_idx)} rows, validation fold has {len(valid_idx)} rows, MAE {mae:.2f}")\n'
            '    print("   groups in the validation fold:", {g: int(n) for g, n in groups.iloc[valid_idx].value_counts().sort_index().items()})\n\n'
            '# ddof=1: the sample standard deviation, divide by k - 1 (np.std divides by k unless you say ddof=1)\n'
            'print(f"5-fold CV mean MAE: {np.mean(cv_scores):.2f}   standard deviation: {np.std(cv_scores, ddof=1):.2f}")\n'
            'print(f"lowest to highest: {min(cv_scores):.2f} to {max(cv_scores):.2f}")')
    nb.read('Pick one fold and check that its validation rows were not among its training rows (the two counts add up to 58). Which groups are in each validation fold? Has the tree already met those machines in training? Is the standard deviation small or large compared with the mean?')
    nb.code('# the one-line shortcut, cross_val_score, gives the same numbers\n'
            'imputer = SimpleImputer(strategy="median")\n'
            'tree = DecisionTreeRegressor(max_depth=4, random_state=17)\n'
            'pipeline = make_pipeline(imputer, tree)\n'
            'cv_scores_auto = -cross_val_score(pipeline, X_train, y_train, cv=KFold(n_splits=5), scoring="neg_mean_absolute_error")   # minus: scikit-learn flips the sign\n'
            'print(f"cross_val_score mean MAE: {cv_scores_auto.mean():.2f}")\n'
            'print("same scores as the loop:", bool(np.allclose(cv_scores_auto, cv_scores)))')
    nb.md('**GroupKFold.** Each fold holds out one whole equipment group as the validation fold. The model is tested on a group it has never met, which is how it will be used on a new machine. Each of E1 to E4 is held out once; scikit-learn chooses the order (it balances the fold sizes), so we print the results sorted by group name.')
    nb.code('group_kfold = GroupKFold(n_splits=4)\n'
            'results = {}\n'
            'for train_idx, valid_idx in group_kfold.split(X_train, y_train, groups):\n'
            '    held_out = groups.iloc[valid_idx].iloc[0]                  # the name of the held-out group\n'
            '    tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))\n'
            '    tree_model.fit(X_train.iloc[train_idx], y_train.iloc[train_idx])\n'
            '    results[held_out] = mean_absolute_error(y_train.iloc[valid_idx], tree_model.predict(X_train.iloc[valid_idx]))\n\n'
            'for name in sorted(results):\n'
            '    print(f"held-out group {name}: MAE {results[name]:.2f}")\n'
            'group_values = list(results.values())\n'
            'print(f"GroupKFold 4-fold CV mean MAE: {np.mean(group_values):.2f}   standard deviation: {np.std(group_values, ddof=1):.2f}")\n\n'
            'cv_scores_group = -cross_val_score(pipeline, X_train, y_train, cv=group_kfold, groups=groups, scoring="neg_mean_absolute_error")\n'
            'print(f"cross_val_score mean MAE: {cv_scores_group.mean():.2f}   standard deviation: {cv_scores_group.std(ddof=1):.2f}")\n\n'
            '# the single split from Class 1, for comparison\n'
            'single_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17)).fit(X_train, y_train)\n'
            f'print(f"one split, group E5: MAE {{mean_absolute_error(y_valid, single_model.predict(X_valid)):.2f}} {unit}")')
    nb.read('Which held-out group is hardest? How does the one-split score for E5 compare with the GroupKFold mean? What does the standard deviation tell you about how far to trust one number?')
    c5, g = N['cv5'], N['grp']
    nb.md(f'**CHECK.** You should see: 5-fold mean {d2(c5["mean"])} and standard deviation {d2(c5["std"])}; GroupKFold mean {d2(g["mean"])} and standard deviation {d2(g["std"])}; one split on E5 {d2(N["tree4_valid"])} {unit}.')
    nb.change('Change `max_depth=4` to your chosen depth from Step 2 in the plain 5-fold loop (rows cut in order, no shuffle) and run it again. Does the mean error get smaller or larger? Does the standard deviation change?')

    nb.step(4, 'Plant three kinds of data leakage on purpose', 'Data leakage makes the score look better than it really is. We plant each of the three kinds from the slides and read the damage.')
    nb.md('**Leakage 1, train-test contamination: the validation rows are copied into the training set.** We use the max_depth 10 tree so that overfitting is easy.')
    nb.predict('The leaky tree was trained on the validation rows. What validation error do you expect from it?')
    nb.code('honest_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=10, random_state=17))\n'
            'honest_model.fit(X_train, y_train)\n'
            'honest_mae = mean_absolute_error(y_valid, honest_model.predict(X_valid))\n\n'
            'X_leaky = pd.concat([X_train, X_valid])         # the mistake: validation rows join the training set\n'
            'y_leaky = pd.concat([y_train, y_valid])\n'
            'leaky_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=10, random_state=17))\n'
            'leaky_model.fit(X_leaky, y_leaky)\n'
            'leaky_mae = mean_absolute_error(y_valid, leaky_model.predict(X_valid))\n\n'
            f'print(f"Honest validation MAE: {{honest_mae:.2f}} {unit}")\n'
            f'print(f"Leaky validation MAE: {{leaky_mae:.2f}} {unit}")')
    nb.read('Which score would you quote to a client? Which score would predict a brand new machine?')
    nb.md('**Leakage 2, preprocessing leakage: the imputer is fitted on rows outside the training set.** One missing value (ambient_c in one training row) is filled by median imputation. The honest fill uses the median of the training rows. The leaky fill uses the median of the training and validation rows together.')
    nb.predict('Will the leaky median change the validation MAE? By a lot, a little, or not at all?')
    nb.code('X_all = pd.concat([X_train, X_valid])\n'
            'fill_train = X_train.median()          # median of each column, from the training rows only\n'
            'fill_all = X_all.median()              # the mistake: validation rows help decide the fill\n'
            'print(f"fill for ambient_c, training rows only: {fill_train[\'ambient_c\']:.2f}")\n'
            'print(f"fill for ambient_c, training and validation rows (leaky): {fill_all[\'ambient_c\']:.2f}")\n\n'
            'tree_train_fill = DecisionTreeRegressor(max_depth=10, random_state=17).fit(X_train.fillna(fill_train), y_train)\n'
            'tree_all_fill = DecisionTreeRegressor(max_depth=10, random_state=17).fit(X_train.fillna(fill_all), y_train)\n'
            f'print(f"MAE with the honest fill: {{mean_absolute_error(y_valid, tree_train_fill.predict(X_valid.fillna(fill_train))):.2f}} {unit}")\n'
            f'print(f"MAE with the leaky fill: {{mean_absolute_error(y_valid, tree_all_fill.predict(X_valid.fillna(fill_all))):.2f}} {unit}")')
    nb.read('Compare the two fill values, then the two scores. Was your prediction right? Does a score that did not move prove the leaky fill is safe? (Hint: how many values are missing here?) Which tool fits the imputer on the training folds only, in every fold?')
    nb.md('**Leakage 3, target leakage: a feature built from the target.** We add the target rounded to a whole number as a feature.')
    nb.predict('What validation MAE will the depth-4 tree give with this feature: about the same as without it, or much smaller?')
    nb.code('X_train_leak = X_train.copy()\nX_valid_leak = X_valid.copy()\n'
            'X_train_leak["target_rounded"] = y_train.round()       # the mistake: built from the target\n'
            'X_valid_leak["target_rounded"] = y_valid.round()\n'
            'leak_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))\n'
            'leak_model.fit(X_train_leak, y_train)\n'
            f'print(f"Depth-4 tree with the target feature: {{mean_absolute_error(y_valid, leak_model.predict(X_valid_leak)):.2f}} {unit}")\n'
            'clean_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17)).fit(X_train, y_train)\n'
            f'print(f"Depth-4 tree, honest features: {{mean_absolute_error(y_valid, clean_model.predict(X_valid)):.2f}} {unit}")')
    nb.read('The first score looks wonderful. Why could you never use that feature when a new reading arrives?')
    nb.md('**THINK.** The five checklist questions from the slides:\n\n'
          '1. Was the score measured on held-out data (rows the model never saw)?\n'
          '2. Were the imputer and the scaler fitted on the training set only (no preprocessing leakage)?\n'
          '3. Is every feature available at the moment you need the prediction, and none built from the target (no target leakage)?\n'
          '4. Is the test set (group E6) still sealed, to be opened once after the final choice?\n'
          '5. Is the score a cross-validation mean, shown with its standard deviation?\n\n'
          'Write down which question each of the three kinds of leakage breaks.\n\n> My answer: ')
    lk = N['leak']
    nb.md(f'**CHECK.** You should see: honest {d2(lk["honest"])} and leaky {d2(lk["leaky"])} {unit}; fills {d2(N["fill"]["train"])} and {d2(N["fill"]["trva"])}; target feature {d2(N["disguise"])} {unit}.')

    nb.step(5, 'Reproducibility: the random seed and a run record', 'The random seed (random_state in scikit-learn) makes a random choice repeat exactly. The same seed gives the same numbers. A different seed can give a different number.')
    nb.predict('If we change only the random seed, will the max_depth 10 tree score change? Will the shuffled 5-fold average change?')
    nb.code('for seed in [1, 17, 99]:\n'
            '    tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=10, random_state=seed))\n'
            '    tree_model.fit(X_train, y_train)\n'
            f'    print(f"tree random_state {{seed}}: validation MAE {{mean_absolute_error(y_valid, tree_model.predict(X_valid)):.2f}} {unit}")\n\n'
            'pipeline = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))\n'
            'for seed in [1, 17, 99]:\n'
            '    kfold_shuffled = KFold(n_splits=5, shuffle=True, random_state=seed)          # shuffle the rows before cutting them into folds\n'
            '    cv_scores = -cross_val_score(pipeline, X_train, y_train, cv=kfold_shuffled, scoring="neg_mean_absolute_error")\n'
            '    print(f"shuffled 5-fold, random_state {seed}: mean MAE {cv_scores.mean():.2f}")')
    nb.read('Which numbers moved? By how much? Why must a result always be quoted together with its random seed? What does the range of the three numbers tell you about luck?')
    nb.md('**Does the chosen max_depth move with the seed?** We rerun the Step 2 rule (simplest depth within 5 percent of the lowest validation MAE) with each seed.')
    nb.predict('Will the rule choose the same max_depth for every seed?')
    nb.code('for seed in [1, 17, 99]:\n'
            '    seed_maes = []\n'
            '    for depth in depths:\n'
            '        tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=depth, random_state=seed))\n'
            '        seed_maes.append(mean_absolute_error(y_valid, tree_model.fit(X_train, y_train).predict(X_valid)))\n'
            '    seed_lowest = min(seed_maes)\n'
            '    seed_choice = min(d for d, v in zip(depths, seed_maes) if v <= seed_lowest * 1.05)\n'
            '    print(f"random_state {seed}: chosen max_depth {seed_choice}")')
    nb.read(f'With only {f["b"]["n_va"]} validation rows, is the chosen depth a fact about the data, or partly luck? How does cross-validation help?')
    picks = ', '.join(str(N['seed_pick'][sd]) for sd in c3.SEEDS)
    nb.md(f'**CHECK.** You should see: depth-10 tree {", ".join(d2(N["seed_tree"][sd]) for sd in c3.SEEDS)} {unit}; shuffled 5-fold {", ".join(d2(N["seed_cv"][sd]) for sd in c3.SEEDS)}; chosen max_depth {picks} for random_state 1, 17, 99.')
    nb.change('Add 0 and 42 to the list of seeds and run the cell again. How many different depths does the rule choose now?')
    nb.code('import platform\nimport hashlib\nimport sklearn\n\n'
            'fingerprint = hashlib.md5(open("engineering_data.csv", "rb").read()).hexdigest()[:8]\n'
            'print("RUN RECORD")\n'
            'print("data file: engineering_data.csv,", len(raw_data), "rows, fingerprint", fingerprint)\n'
            'print("rows after cleaning in Class 1:", len(modelling_data), "(training", len(training_data), ", validation", len(validation_data), ", test", len(test_data), ")")\n'
            'print("split: training E1 to E4, validation E5, test E6 sealed")\n'
            'print("random seed: random_state = 17 for trees and for the shuffled folds (Step 5 also tries 1 and 99)")\n'
            'print("python", platform.python_version(), "| numpy", np.__version__, "| pandas", pd.__version__, "| scikit-learn", sklearn.__version__)')
    nb.md('Copy this record under every result you report. Your version numbers may differ from your neighbour\'s.')

    nb.step(6, 'Functions on records, as in the project', 'The project gives you rows as **records**: each row is a dictionary (the keys are the column names), and a table is a list of dictionaries. Its functions take records and return plain lists. This step practises that form. '
            '`predict_records` wraps a pipeline in a function: it trains on a list of training records and returns one prediction per new record, in order. '
            'A *list comprehension* builds a new list in one line: `[expression for item in a_list if condition]`. `sorted(a_list, key=lambda r: ...)` sorts the items by the value that the small `lambda` function gives for each one.')
    nb.predict('Three models: linear regression, the depth-4 tree and the tree with your chosen depth. Which one will come first when we sort by validation MAE?')
    nb.code('record_columns = ["record_id", "equipment_id", "load_pct", "ambient_c", "target"]\n'
            'train_records = training_data[record_columns].to_dict("records")     # a list of dictionaries, one per row\n'
            'valid_records = validation_data[record_columns].to_dict("records")\n'
            'print("training records:", len(train_records))\n'
            'print("first training record:", train_records[0])\n\n'
            'def predict_records(model, training_records, new_records):\n'
            '    """Train the pipeline on a list of records and return one prediction per new record, in order."""\n'
            '    table = pd.DataFrame(training_records)\n'
            '    new_table = pd.DataFrame(new_records)\n'
            '    model.fit(table[feature_columns], table["target"])\n'
            '    return model.predict(new_table[feature_columns]).tolist()\n\n'
            'valid_features = [{key: value for key, value in r.items() if key != "target"} for r in valid_records]   # the new rows have no target\n'
            'valid_actual = [r["target"] for r in valid_records]\n\n'
            'models = {"Linear regression": make_pipeline(SimpleImputer(strategy="median"), LinearRegression()),\n'
            '          "Decision tree, depth 4": make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17)),\n'
            '          "Decision tree, chosen depth": make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=best_depth, random_state=17))}\n\n'
            'model_results = []\n'
            'for name, model in models.items():\n'
            '    predictions = predict_records(model, train_records, valid_features)\n'
            '    errors = [abs(a - p) for a, p in zip(valid_actual, predictions)]      # a list comprehension: one error per row\n'
            '    model_results.append({"name": name, "validation_mae": sum(errors) / len(errors)})\n\n'
            'ranked = sorted(model_results, key=lambda r: (r["validation_mae"], r["name"]))   # smallest MAE first; a tie goes to the name\n'
            'for r in ranked:\n'
            f'    print(f"{{r[\'name\']}}: validation MAE {{r[\'validation_mae\']:.2f}} {unit}")\n'
            'print("first after sorting:", ranked[0]["name"])')
    nb.read('Are the three MAEs the same as in Steps 2 and 3? Why does `valid_features` leave out the target? What does `ranked[0]` hold?')
    cur = {d: v for d, _, v in N['curve']}
    first = min([('Linear regression', N['line_mae']), ('Decision tree, depth 4', N['tree4_valid']), ('Decision tree, chosen depth', cur[N['best']])], key=lambda x: (x[1], x[0]))[0]
    nb.md(f'**CHECK.** You should see: {f["b"]["n_tr"]} training records; linear regression {d2(N["line_mae"])}, depth-4 tree {d2(N["tree4_valid"])}, chosen depth {d2(cur[N["best"]])} {unit}; first after sorting: {first}.')
    nb.change('Change the key to `key=lambda r: r["name"]` and run the cell again. What order do you get now, and why is it a poor way to rank models?')

    nb.step(7, 'Your conclusion, and save your work', 'Write three sentences: which max_depth you chose and why, what cross-validation says about how far to trust the score, and which kind of data leakage surprised you most.\n\n> My conclusion: \n\n'
            '**What this does not prove.** The data are synthetic teaching data, the validation group has only a few rows, and the test set (group E6) has not been used. '
            'Choose **Runtime, then Restart session and run all**. If every cell runs without an error, choose **File, then Save a copy in Drive**. Keep the notebook: the rehearsal and the project use the same steps.')
    return nb


def CHECK(code, res, f):
    """Every number the notebook prints must equal the reference value used on the slides."""
    N = c3.refs(f)
    text = '\n'.join(o for _, o, _ in res)
    b = f['b']
    want = [f'rows left to model with: {b["n_clean"]}', f'training, validation, test rows: {b["n_tr"]} {b["n_va"]} {b["n_te"]}']
    for d, t, v in N['curve']:
        want.append(f'depth {d:2d}  training {t:.2f}  validation {v:.2f}  generalisation gap {v - t:.2f}')
    want += [f'limit (lowest x 1.05): {N["lowest"] * c3.TOL:.3f}'] + [f'depth {d:2d}: validation {v:.3f} ' + ('passes' if v <= N['lowest'] * c3.TOL else 'fails') for d, _, v in N['curve']]
    want += [f'lowest validation MAE: {N["lowest"]:.2f} {f["unit"]}', f'chosen depth: {N["best"]}', f'Linear regression, validation MAE: {N["line_mae"]:.2f} {f["unit"]}']
    c5, g = N['cv5'], N['grp']
    for i, (sc, (a, t)) in enumerate(zip(c5['scores'], c5['sizes']), 1):
        want.append(f'fold {i}: train on {a} rows, validation fold has {t} rows, MAE {sc:.2f}')
        want.append(f'   groups in the validation fold: {c5["groups"][i - 1]}')
    want += [f'5-fold CV mean MAE: {c5["mean"]:.2f}   standard deviation: {c5["std"]:.2f}', f'lowest to highest: {c5["lo"]:.2f} to {c5["hi"]:.2f}', f'cross_val_score mean MAE: {c5["mean"]:.2f}', 'same scores as the loop: True']
    for name, v in g['scores'].items():
        want.append(f'held-out group {name}: MAE {v:.2f}')
    want += [f'GroupKFold 4-fold CV mean MAE: {g["mean"]:.2f}   standard deviation: {g["std"]:.2f}', f'cross_val_score mean MAE: {g["mean"]:.2f}   standard deviation: {g["std"]:.2f}', f'one split, group E5: MAE {N["tree4_valid"]:.2f} {f["unit"]}',
             f'Honest validation MAE: {N["leak"]["honest"]:.2f} {f["unit"]}', f'Leaky validation MAE: {N["leak"]["leaky"]:.2f} {f["unit"]}',
             f"fill for ambient_c, training rows only: {N['fill']['train']:.2f}", f"fill for ambient_c, training and validation rows (leaky): {N['fill']['trva']:.2f}",
             f'MAE with the honest fill: {N["fill"]["mae_train"]:.2f} {f["unit"]}', f'MAE with the leaky fill: {N["fill"]["mae_all"]:.2f} {f["unit"]}',
             f'Depth-4 tree with the target feature: {N["disguise"]:.2f} {f["unit"]}', f'Depth-4 tree, honest features: {N["tree4_valid"]:.2f} {f["unit"]}']
    for sd in c3.SEEDS:
        want.append(f'tree random_state {sd}: validation MAE {N["seed_tree"][sd]:.2f} {f["unit"]}')
        want.append(f'shuffled 5-fold, random_state {sd}: mean MAE {N["seed_cv"][sd]:.2f}')
        want.append(f'random_state {sd}: chosen max_depth {N["seed_pick"][sd]}')
    cur = {d: v for d, _, v in N['curve']}
    trio = [('Linear regression', N['line_mae']), ('Decision tree, depth 4', N['tree4_valid']), ('Decision tree, chosen depth', cur[N['best']])]
    want.append(f'training records: {b["n_tr"]}')
    for name, v in trio:
        want.append(f'{name}: validation MAE {v:.2f} {f["unit"]}')
    want.append('first after sorting: ' + min(trio, key=lambda x: (x[1], x[0]))[0])
    want.append(f'rows after cleaning in Class 1: {b["n_clean"]} (training {b["n_tr"]} , validation {b["n_va"]} , test {b["n_te"]} )')
    csv = Path(__file__).resolve().parents[1] / 'data' / code / 'engineering_data.csv'
    want.append(f'engineering_data.csv, {N["n_rows"]} rows, fingerprint {hashlib.md5(csv.read_bytes()).hexdigest()[:8]}')
    # the slide claims that depend on the notebook output
    probs = [f'missing expected output: {w}' for w in want if w not in text]
    if len(set(round(v, 2) for v in N['seed_tree'].values())) < 2:
        probs.append('seed demonstration: the three tree scores are all equal')
    return probs
