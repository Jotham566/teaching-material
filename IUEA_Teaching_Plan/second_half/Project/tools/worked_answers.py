"""The worked answers for the lecturer (16 November 2026): the code typed live in the revision class, and the run-all answer notebooks.

Plain names, one short comment per step, only what students have been taught (pandas, matplotlib, make_pipeline, SimpleImputer, the three
regression models, logistic regression, the confusion matrix). Each block stores exactly the result names the task asks for, so the same code
earns full marks in the project (with random_state=17) and runs the rehearsal (random_state=29).
"""

CLEAN = '''# Look first: how many problems are there?
print("Duplicate houses:", houses_raw.duplicated().sum(), "| no price:", houses_raw[H_TARGET].isna().sum())
print("Duplicate machines:", machines_raw.duplicated().sum(), "| no label:", machines_raw[M_TARGET].isna().sum())

# Work on copies, so the raw tables never change
houses = houses_raw.copy()
machines = machines_raw.copy()

# 1. Remove duplicate rows
houses = houses.drop_duplicates()
machines = machines.drop_duplicates()

# 2. Remove rows with no target value
houses = houses.dropna(subset=[H_TARGET])
machines = machines.dropna(subset=[M_TARGET])

# 3. Keep only rows with possible values
area_ok = houses["living_area_m2"] > 0
year_ok = houses["year_built"] <= 2010
houses = houses[area_ok & year_ok]

torque_ok = machines["torque_nm"] > 0
speed_ok = machines["rotation_speed_rpm"] > 0
machines = machines[torque_ok & speed_ok].copy()

# 4. Product type as a number
machines["product_type"] = machines["product_type"].map({"L": 0, "M": 1, "H": 2})

print("Houses:", houses_raw.shape, "->", houses.shape)
print("Machines:", machines_raw.shape, "->", machines.shape)

# Chart 1: does a bigger house sell for more?
plt.figure()
plt.scatter(houses["living_area_m2"], houses[H_TARGET], s=4)
plt.title("Chart 1: sale price against living area")
plt.xlabel("Living area (m2)")
plt.ylabel("Sale price (USD)")
plt.show()
'''

SPLIT = '''# 20% test first, then 25% of the rest for validation: 60 / 20 / 20
houses_test = houses.sample(frac=0.2, random_state=SEED)
houses_rest = houses.drop(houses_test.index)
houses_valid = houses_rest.sample(frac=0.25, random_state=SEED)
houses_train = houses_rest.drop(houses_valid.index)

machines_test = machines.sample(frac=0.2, random_state=SEED)
machines_rest = machines.drop(machines_test.index)
machines_valid = machines_rest.sample(frac=0.25, random_state=SEED)
machines_train = machines_rest.drop(machines_valid.index)

print("Houses   train, valid, test:", len(houses_train), len(houses_valid), len(houses_test))
print("Machines train, valid, test:", len(machines_train), len(machines_valid), len(machines_test))
'''

MODELS = '''# Features (X) and target (y)
X_train, y_train = houses_train[H_FEATURES], houses_train[H_TARGET]
X_valid, y_valid = houses_valid[H_FEATURES], houses_valid[H_TARGET]

# Each model first fills gaps with medians learned from the training rows only
baseline_model = make_pipeline(SimpleImputer(strategy="median"), DummyRegressor())
linear_model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))

# Learn from the training rows
baseline_model.fit(X_train, y_train)
linear_model.fit(X_train, y_train)
tree_model.fit(X_train, y_train)

# Predict the validation rows
baseline_pred = baseline_model.predict(X_valid)
linear_pred = linear_model.predict(X_valid)
tree_pred = tree_model.predict(X_valid)

# MAE: the average error. RMSE: like MAE, but big errors count more
baseline_mae = np.mean(np.abs(y_valid - baseline_pred))
linear_mae = np.mean(np.abs(y_valid - linear_pred))
tree_mae = np.mean(np.abs(y_valid - tree_pred))
baseline_rmse = np.sqrt(np.mean((y_valid - baseline_pred) ** 2))
linear_rmse = np.sqrt(np.mean((y_valid - linear_pred) ** 2))
tree_rmse = np.sqrt(np.mean((y_valid - tree_pred) ** 2))
print("MAE  baseline, linear, tree:", round(baseline_mae), round(linear_mae), round(tree_mae))
print("RMSE baseline, linear, tree:", round(baseline_rmse), round(linear_rmse), round(tree_rmse))

# Chart 2: which model makes the smallest error?
plt.figure()
plt.bar(["baseline", "linear", "tree"], [baseline_mae, linear_mae, tree_mae])
plt.title("Chart 2: validation MAE of the three models")
plt.xlabel("Model")
plt.ylabel("MAE (USD)")
plt.show()
'''

ENCODED = '''# Numbers: fill gaps with the median. Text: fill with the commonest value, then one 0/1 column per category
prepare_columns = make_column_transformer(
    (SimpleImputer(strategy="median"), H_FEATURES),
    (make_pipeline(SimpleImputer(strategy="most_frequent"), OneHotEncoder(handle_unknown="ignore")), TEXT_FEATURES))
encoded_model = make_pipeline(prepare_columns, LinearRegression())

all_columns = H_FEATURES + TEXT_FEATURES
encoded_model.fit(houses_train[all_columns], houses_train[H_TARGET])
encoded_pred = encoded_model.predict(houses_valid[all_columns])
encoded_mae = np.mean(np.abs(houses_valid[H_TARGET] - encoded_pred))
print("MAE with text columns:", round(encoded_mae), "| without:", round(linear_mae))
'''

WARNING = '''# A warning is a real failure (failure is 1)
y_train_warn = (machines_train[M_TARGET] >= M_LIMIT).astype(int)
y_valid_warn = (machines_valid[M_TARGET] >= M_LIMIT).astype(int)

# Fill gaps, put the features on one scale, then logistic regression
warning_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
warning_model.fit(machines_train[M_FEATURES], y_train_warn)

# The probability of a failure for each validation run; warn at 0.5 or more
warning_proba = warning_model.predict_proba(machines_valid[M_FEATURES])[:, 1]
warned = (warning_proba >= THRESHOLD).astype(int)

# Confusion matrix: ravel() gives tn, fp, fn, tp in this order
tn, fp, fn, tp = confusion_matrix(y_valid_warn, warned, labels=[0, 1]).ravel()
precision = precision_score(y_valid_warn, warned, zero_division=0)   # of our warnings, how many were right
recall = recall_score(y_valid_warn, warned, zero_division=0)         # of real failures, how many we caught
print("TP", tp, "FP", fp, "FN", fn, "TN", tn, "| precision", round(precision, 2), "| recall", round(recall, 2))
'''

CHOOSE = '''# The supplied rule: MAE within the limit, fast enough, then the smallest MAE
chosen_model = choose_model({"baseline": baseline_mae, "linear": linear_mae, "tree": tree_mae})
print("Chosen model:", chosen_model)
'''

TEST = '''# Only now, after the choice: refit on training + validation rows, then score the test rows once
houses_dev = pd.concat([houses_train, houses_valid])
model_types = {"baseline": DummyRegressor(),
               "linear": LinearRegression(),
               "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final_model = make_pipeline(SimpleImputer(strategy="median"), model_types[chosen_model])
final_model.fit(houses_dev[H_FEATURES], houses_dev[H_TARGET])
test_mae = np.mean(np.abs(houses_test[H_TARGET] - final_model.predict(houses_test[H_FEATURES])))

machines_dev = pd.concat([machines_train, machines_valid])
final_warning_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
final_warning_model.fit(machines_dev[M_FEATURES], (machines_dev[M_TARGET] >= M_LIMIT).astype(int))
test_warned = (final_warning_model.predict_proba(machines_test[M_FEATURES])[:, 1] >= THRESHOLD).astype(int)
test_recall = recall_score((machines_test[M_TARGET] >= M_LIMIT).astype(int), test_warned, zero_division=0)
print("Test MAE:", round(test_mae), "| test recall:", round(test_recall, 2))
'''

BY_TASK = {'clean': CLEAN, 'split': SPLIT, 'regression': MODELS, 'encoded': ENCODED, 'warning': WARNING, 'choose': CHOOSE, 'test': TEST}


def answer(key, seed):
    return BY_TASK[key].replace('SEED', str(seed))
