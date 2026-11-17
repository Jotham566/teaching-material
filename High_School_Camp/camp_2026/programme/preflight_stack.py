#!/usr/bin/env python3
"""Run once on every learner laptop (and the instructor's) before the camp.

Imports each library the camp teaches, prints its version, and exercises one
real function from each, with a non-interactive plotting backend so no window
opens. Exit code 0 means the laptop is ready.

    python preflight_stack.py            core stack
    python preflight_stack.py --tf       also checks TensorFlow/Keras (instructor laptop only)
"""
import sys, importlib, tempfile, os

ok = True
def step(name, fn):
    global ok
    try:
        detail = fn()
        print(f"PASS  {name}" + (f"  [{detail}]" if detail else ""))
    except Exception as e:
        ok = False
        print(f"FAIL  {name}  [{type(e).__name__}: {e}]")

print("Python", sys.version.split()[0])
def ver(m): return importlib.import_module(m).__version__

import matplotlib; matplotlib.use("Agg")
tmp = tempfile.mkdtemp()

def t_numpy():
    import numpy as np
    a = np.array([2, 4, 6]); assert (a * 2).tolist() == [4, 8, 12] and np.median(a) == 4 and float(np.dot(a, [1, 1, 1])) == 12
    return ver("numpy")
def t_pandas():
    import pandas as pd
    df = pd.DataFrame({"item": ["Book", "Pen", "Book"], "units": [2, 5, 3]})
    assert df.groupby("item")["units"].sum().to_dict() == {"Book": 5, "Pen": 5}
    p = os.path.join(tmp, "t.csv"); df.to_csv(p, index=False); assert pd.read_csv(p).shape == (3, 2)
    return ver("pandas")
def t_mpl():
    import matplotlib.pyplot as plt
    plt.bar(["a", "b"], [1, 2]); plt.savefig(os.path.join(tmp, "m.png")); plt.close("all")
    return ver("matplotlib")
def t_sns():
    import seaborn as sns, pandas as pd
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [2, 4, 5, 4, 6, 9], "g": list("aabbcc")})
    sns.histplot(data=df, x="x"); sns.boxplot(data=df, x="g", y="y"); sns.heatmap(df[["x", "y"]].corr(), annot=True)
    import matplotlib.pyplot as plt; plt.savefig(os.path.join(tmp, "s.png")); plt.close("all")
    return ver("seaborn")
def t_sk():
    import numpy as np
    from sklearn.linear_model import LinearRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, confusion_matrix
    m = LinearRegression().fit([[1], [2], [3]], [2, 4, 6]); assert abs(m.predict([[4]])[0] - 8) < 1e-9
    d = load_iris(); Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.2, random_state=7, stratify=d.target)
    t = DecisionTreeClassifier(max_depth=2, random_state=7).fit(Xtr, ytr)
    assert confusion_matrix(yte, t.predict(Xte)).shape == (3, 3)
    return f"{ver('sklearn')}, iris accuracy {accuracy_score(yte, t.predict(Xte)):.2f}"
def t_nb():
    import notebook, ipykernel
    return f"notebook {ver('notebook')}, ipykernel {ver('ipykernel')}"
def t_tf():
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    import tensorflow as tf
    from tensorflow import keras
    m = keras.Sequential([keras.layers.Input((2,)), keras.layers.Dense(4, activation="relu"), keras.layers.Dense(1)])
    m.compile("adam", "mse"); m.fit([[0, 0], [1, 1]], [0, 1], epochs=1, verbose=0)
    return f"tensorflow {tf.__version__}, keras {keras.__version__}"

for n, f in (("numpy", t_numpy), ("pandas", t_pandas), ("matplotlib", t_mpl), ("seaborn", t_sns),
             ("scikit-learn", t_sk), ("jupyter notebook", t_nb)):
    step(n, f)
if "--tf" in sys.argv:
    step("tensorflow + keras (instructor only)", t_tf)
print("READY" if ok else "NOT READY: fix the FAIL lines before class")
sys.exit(0 if ok else 1)
