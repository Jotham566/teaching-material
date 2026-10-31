from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=.2, random_state=7, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=.25, random_state=7, stratify=y_dev)
assert (len(X_train), len(X_val), len(X_test)) == (90, 30, 30)
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
print("Validation baseline", accuracy_score(y_val, baseline.predict(X_val)))
models = [DecisionTreeClassifier(max_depth=d, random_state=7).fit(X_train, y_train) for d in [1, 3]]
scores = [accuracy_score(y_val, m.predict(X_val)) for m in models]
chosen = max(range(len(models)), key=lambda i: scores[i])
print("Validation scores", scores, "Chosen depth", [1, 3][chosen])
print("Final test accuracy", accuracy_score(y_test, models[chosen].predict(X_test)))
print(confusion_matrix(y_test, models[chosen].predict(X_test)))
