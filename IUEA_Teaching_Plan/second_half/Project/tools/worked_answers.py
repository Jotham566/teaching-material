"""The worked answers for the lecturer (16 November 2026): the code typed live in the revision class, and the run-all answer notebooks.

Two separate questions, no baseline model. Plain names, one short comment per step, only what students have been taught (pandas,
matplotlib, make_pipeline, SimpleImputer, linear regression, decision trees, logistic regression, the confusion matrix). Each block stores
exactly the result names the task asks for, so the same code earns full marks in the project (random_state=17) and runs the rehearsal (29).
"""

CLEAN_H = '''# Look first: how many problems are there?
print("Duplicate houses:", houses_raw.duplicated().sum(), "| no price:", houses_raw[H_TARGET].isna().sum())

# Work on a copy, so the raw table never changes
houses = houses_raw.copy()

# 1. Remove duplicate rows
houses = houses.drop_duplicates()

# 2. Remove rows with no price
houses = houses.dropna(subset=[H_TARGET])

# 3. Keep only rows with possible values
area_ok = houses["living_area_m2"] > 0
year_ok = houses["year_built"] <= 2010
houses = houses[area_ok & year_ok]
print("Houses:", houses_raw.shape, "->", houses.shape)

# Chart 1: does a bigger house sell for more?
plt.figure()
plt.scatter(houses["living_area_m2"], houses[H_TARGET], s=4)
plt.title("Chart 1: sale price against living area")
plt.xlabel("Living area (m2)")
plt.ylabel("Sale price (USD)")
plt.show()
'''

SPLIT_H = '''# 20% test first, then 25% of the rest for validation: 60 / 20 / 20
houses_test = houses.sample(frac=0.2, random_state=SEED)
houses_rest = houses.drop(houses_test.index)
houses_valid = houses_rest.sample(frac=0.25, random_state=SEED)
houses_train = houses_rest.drop(houses_valid.index)
print("Houses train, valid, test:", len(houses_train), len(houses_valid), len(houses_test))
'''

MODELS = '''# Features (X) and target (y)
X_train, y_train = houses_train[H_FEATURES], houses_train[H_TARGET]
X_valid, y_valid = houses_valid[H_FEATURES], houses_valid[H_TARGET]

# Each model first fills gaps with medians learned from the training rows only
linear_model = make_pipeline(SimpleImputer(strategy="median"), LinearRegression())
tree_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeRegressor(max_depth=4, random_state=17))

# Learn from the training rows, then predict the validation rows
linear_model.fit(X_train, y_train)
tree_model.fit(X_train, y_train)
linear_pred = linear_model.predict(X_valid)
tree_pred = tree_model.predict(X_valid)

# MAE: the average error. RMSE: like MAE, but big errors count more
linear_mae = np.mean(np.abs(y_valid - linear_pred))
tree_mae = np.mean(np.abs(y_valid - tree_pred))
linear_rmse = np.sqrt(np.mean((y_valid - linear_pred) ** 2))
tree_rmse = np.sqrt(np.mean((y_valid - tree_pred) ** 2))
print("MAE  linear, tree:", round(linear_mae), round(tree_mae))
print("RMSE linear, tree:", round(linear_rmse), round(tree_rmse))

# Chart 2: which model makes the smaller error?
plt.figure()
plt.bar(["linear", "tree"], [linear_mae, tree_mae])
plt.title("Chart 2: validation MAE of the two models")
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

TEST_H = '''# The supplied rule: MAE within the limit, fast enough, then the smaller MAE
chosen_house_model = choose_model({"linear": linear_mae, "tree": tree_mae})
print("Chosen house model:", chosen_house_model)

# Only now: refit on training + validation rows, then score the test rows once
houses_dev = pd.concat([houses_train, houses_valid])
house_models = {"linear": LinearRegression(),
                "tree": DecisionTreeRegressor(max_depth=4, random_state=17)}
final_house_model = make_pipeline(SimpleImputer(strategy="median"), house_models[chosen_house_model])
final_house_model.fit(houses_dev[H_FEATURES], houses_dev[H_TARGET])
test_mae = np.mean(np.abs(houses_test[H_TARGET] - final_house_model.predict(houses_test[H_FEATURES])))
print("Test MAE:", round(test_mae))
'''

CLEAN_M = '''# Look first, then the same three steps as for the houses
print("Duplicate machines:", machines_raw.duplicated().sum(), "| no label:", machines_raw[M_TARGET].isna().sum())
machines = machines_raw.copy()
machines = machines.drop_duplicates()
machines = machines.dropna(subset=[M_TARGET])

torque_ok = machines["torque_nm"] > 0
speed_ok = machines["rotation_speed_rpm"] > 0
machines = machines[torque_ok & speed_ok].copy()

# Product type as a number
machines["product_type"] = machines["product_type"].map({"L": 0, "M": 1, "H": 2})
print("Machines:", machines_raw.shape, "->", machines.shape)
'''

SPLIT_M = '''# The same rule as for the houses
machines_test = machines.sample(frac=0.2, random_state=SEED)
machines_rest = machines.drop(machines_test.index)
machines_valid = machines_rest.sample(frac=0.25, random_state=SEED)
machines_train = machines_rest.drop(machines_valid.index)
print("Machines train, valid, test:", len(machines_train), len(machines_valid), len(machines_test))
'''

CLASSIFY = '''# A warning is a real failure (failure is 1)
y_train_warn = (machines_train[M_TARGET] >= M_LIMIT).astype(int)
y_valid_warn = (machines_valid[M_TARGET] >= M_LIMIT).astype(int)

# Model 1, logistic regression: fill gaps, put features on one scale, then a probability; warn at 0.5 or more
logistic_model = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000))
logistic_model.fit(machines_train[M_FEATURES], y_train_warn)
logistic_proba = logistic_model.predict_proba(machines_valid[M_FEATURES])[:, 1]
logistic_warn = (logistic_proba >= THRESHOLD).astype(int)

# Model 2, decision tree: answers 0 or 1 directly (no scaling needed)
tree_clf_model = make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17))
tree_clf_model.fit(machines_train[M_FEATURES], y_train_warn)
tree_warn = tree_clf_model.predict(machines_valid[M_FEATURES])

# Confusion matrix: ravel() gives tn, fp, fn, tp in this order
logistic_counts = confusion_matrix(y_valid_warn, logistic_warn, labels=[0, 1]).ravel()
tree_counts = confusion_matrix(y_valid_warn, tree_warn, labels=[0, 1]).ravel()

# Precision: of our warnings, how many were right. Recall: of real failures, how many we caught. F1: balances the two
logistic_precision = precision_score(y_valid_warn, logistic_warn, zero_division=0)
logistic_recall = recall_score(y_valid_warn, logistic_warn, zero_division=0)
logistic_f1 = f1_score(y_valid_warn, logistic_warn, zero_division=0)
tree_precision = precision_score(y_valid_warn, tree_warn, zero_division=0)
tree_recall = recall_score(y_valid_warn, tree_warn, zero_division=0)
tree_f1 = f1_score(y_valid_warn, tree_warn, zero_division=0)
print("Logistic tn, fp, fn, tp:", logistic_counts, "| F1:", round(logistic_f1, 3))
print("Tree     tn, fp, fn, tp:", tree_counts, "| F1:", round(tree_f1, 3))
'''

TEST_M = '''# The supplied rule: the higher validation F1
chosen_warning_model = choose_warning_model({"logistic": logistic_f1, "tree": tree_f1})
print("Chosen warning model:", chosen_warning_model)

# Only now: refit on training + validation runs, then score the test runs once
machines_dev = pd.concat([machines_train, machines_valid])
warning_models = {"logistic": make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), LogisticRegression(max_iter=1000)),
                  "tree": make_pipeline(SimpleImputer(strategy="median"), DecisionTreeClassifier(max_depth=3, random_state=17))}
final_warning_model = warning_models[chosen_warning_model]
final_warning_model.fit(machines_dev[M_FEATURES], (machines_dev[M_TARGET] >= M_LIMIT).astype(int))
test_warn = final_warning_model.predict(machines_test[M_FEATURES])   # 0 or 1 (logistic regression: probability 0.5 or more)
test_f1 = f1_score((machines_test[M_TARGET] >= M_LIMIT).astype(int), test_warn, zero_division=0)
print("Test F1:", round(test_f1, 3))
'''

BY_TASK = {'clean_h': CLEAN_H, 'split_h': SPLIT_H, 'regression': MODELS, 'encoded': ENCODED, 'test_h': TEST_H,
           'clean_m': CLEAN_M, 'split_m': SPLIT_M, 'classify': CLASSIFY, 'test_m': TEST_M}


def answer(key, seed):
    return BY_TASK[key].replace('SEED', str(seed))
