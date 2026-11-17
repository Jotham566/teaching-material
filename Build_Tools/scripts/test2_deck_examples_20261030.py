"""Worked examples for the Week 14 revision slides. Every entry runs as written (checked in
tests/test_test2_weeks8_13.py against a NumPy stand-in, and by verify_week_slides on a Mac with scikit-learn)."""
EXAMPLES = {
"classify": """actual    = [0, 1, 1, 0, 1]
predicted = [0, 1, 0, 0, 1]
pairs = list(zip(actual, predicted))
tp = sum(a == 1 and p == 1 for a, p in pairs)
fn = sum(a == 1 and p == 0 for a, p in pairs)
fp = sum(a == 0 and p == 1 for a, p in pairs)
cost = 5 * fn + fp
print("tp", tp, "fn", fn, "fp", fp)
print("cost", cost)""",
"groupcv": """import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
table = pd.DataFrame({"group": list("AABBCC"),
    "load": [20, 40, 30, 50, 60, 80],
    "target": [10, 21, 14, 26, 29, 41]})
for held_out in "ABC":
    train = table[table["group"] != held_out]
    test = table[table["group"] == held_out]
    model = LinearRegression().fit(train[["load"]], train["target"])
    pred = model.predict(test[["load"]])
    error = mean_absolute_error(test["target"], pred)
    print(held_out, round(error, 2))""",
"ablation": """import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = pd.DataFrame({"load": [20, 30, 40, 50, 60, 70],
    "temp": [20, 25, 22, 30, 28, 35],
    "target": [10.5, 15, 18.7, 25.2, 28.4, 35.9]})
valid = pd.DataFrame({"load": [35, 65], "temp": [24, 32],
    "target": [17.0, 32.6]})
for t in (train, valid):
    t["load_x_temp"] = t["load"] * t["temp"]
for cols in (["load", "temp"], ["load", "temp", "load_x_temp"]):
    model = LinearRegression().fit(train[cols], train["target"])
    pred = model.predict(valid[cols])
    error = mean_absolute_error(valid["target"], pred)
    print(len(cols), "inputs", round(error, 3))""",
"select": """candidates = [
    {"name": "line", "validation_mae": 1.5, "latency_ms": 3},
    {"name": "tree", "validation_mae": 1.2, "latency_ms": 30},
    {"name": "knn", "validation_mae": 1.1, "latency_ms": 12},
    {"name": "mean", "validation_mae": 4.0, "latency_ms": 1}]
kept = [c for c in candidates
        if c["validation_mae"] <= 2.0
        and c["latency_ms"] <= 20]
ranked = sorted(kept, key=lambda c: (
    c["validation_mae"], c["latency_ms"], c["name"]))
print([c["name"] for c in kept])
print(ranked[0]["name"])""",
"ridgeknn_build": """import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    PolynomialFeatures, StandardScaler)
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
ridge = make_pipeline(
    PolynomialFeatures(3, include_bias=False),
    StandardScaler(), Ridge(alpha=1.0))
knn = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(n_neighbors=3))""",
"ridgeknn_score": """from sklearn.metrics import mean_absolute_error
train = pd.DataFrame({
    "load": [20, 30, 40, 50, 60, 70, 80, 90],
    "temp": [22, 30, 25, 35, 28, 33, 26, 31],
    "target": [10.2, 15.8, 19.5, 26.4, 29.1, 35.7, 39.2, 45.6]})
valid = pd.DataFrame({
    "load": [35, 55, 75], "temp": [28, 30, 32],
    "target": [17.9, 28.0, 38.1]})
ridge.fit(train[["load"]], train["target"])
knn.fit(train[["load", "temp"]], train["target"])
for name, model, cols in [("ridge", ridge, ["load"]),
                          ("knn", knn, ["load", "temp"])]:
    pred = model.predict(valid[cols])
    print(name, round(mean_absolute_error(valid["target"], pred), 2))""",
}
