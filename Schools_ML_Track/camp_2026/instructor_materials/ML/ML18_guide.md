# ML18 Instructor guide: Checkpoint two with a locked test

Private. Keep this file out of the student folder.

**Objective.** By the end: you can split data into training, validation and final test, choose a model on validation only, and report one final test result with its limits.

**Question of the day.** Which tree depth is better, and what does a locked test say about it?

Prerequisite: ML17 Mistakes, overfitting and fair comparisons.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 25 | split and plan |
| 15 | break |
| 100 | checkpoint work |
| 15 | explanation of the decision |
| 15 | save and exit check |

Where it overruns: The final-test discipline is the point. Check each learner's order of steps.

## Block A. A three-way split

First lock 20% of the flowers away as the final test, then take a quarter of what remains for validation. stratify keeps each species equally represented in every part.

Ask for the prediction first: Predict the three sizes. They should add up to 150.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=7, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=7, stratify=y_dev)
print(len(X_train), len(X_val), len(X_test))
```

Correct result: The cell prints 90, 30 and 30. stratify=y means each species has the same share in every part: 10 of each species in validation and in the final test. The final test is now locked and must not be used to make any choice.

Investigate, with answers:

- Why are the three parts 60%, 20% and 20%? Answer: 20% is locked away first. A quarter of the other 80% is 20% of the total, which leaves 60%.
- What does stratify do that a plain shuffle does not? Answer: It makes sure each part has the same species mix, so a small part is not accidentally missing one.

Modify: Print how many flowers of species 0 are in the validation part. Answer: Ten.

```python
n_setosa_val = int((y_val == 0).sum())
```

## Block B. Choose on validation, test once

Compare a tree of depth 1 and one of depth 3 on validation only. Freeze the winner. Then run the final test once.

Ask for the prediction first: Predict which depth wins on validation. Write it down before you run.

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
val_baseline = accuracy_score(y_val, baseline.predict(X_val))
tree1 = DecisionTreeClassifier(max_depth=1, random_state=7).fit(X_train, y_train)
tree3 = DecisionTreeClassifier(max_depth=3, random_state=7).fit(X_train, y_train)
score1 = accuracy_score(y_val, tree1.predict(X_val))
score3 = accuracy_score(y_val, tree3.predict(X_val))
if score3 > score1:
    chosen_depth = 3
    final_model = tree3
else:
    chosen_depth = 1
    final_model = tree1
final_acc = accuracy_score(y_test, final_model.predict(X_test))
print(val_baseline, score1, score3, chosen_depth, final_acc)
print(confusion_matrix(y_test, final_model.predict(X_test)))
```

Correct result: The baseline scores exactly one third on validation, because each species is a third. The deeper tree usually wins on validation. The choice is made from the validation scores and then frozen. final_acc is the one honest number: it comes from 30 flowers the choice never saw. The report needs the split sizes, the baseline, both validation scores, the chosen depth, the final accuracy, the confusion matrix and two limitations.

Investigate, with answers:

- Which scores did you use to choose the depth? Answer: The validation scores only.
- What is one limitation of a final test of 30 flowers? Answer: One flower is more than 3 points of accuracy, so the score is unstable.

Modify: Say what you would do if the final test score came out lower than the validation score. Answer: Report it as it is. A lower final score is normal, and changing the choice now would use the test twice.

## Make: reference

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=7, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=7, stratify=y_dev)
tree1 = DecisionTreeClassifier(max_depth=1, random_state=7).fit(X_train, y_train)
tree3 = DecisionTreeClassifier(max_depth=3, random_state=7).fit(X_train, y_train)
scores = [accuracy_score(y_val, tree1.predict(X_val)), accuracy_score(y_val, tree3.predict(X_val))]
print(len(X_train), len(X_val), len(X_test), scores)
```

Evidence to collect: ML18.ipynb: split sizes 90, 30 and 30, baseline, two validation scores, the chosen depth, one final test accuracy, a confusion matrix and two limitations.

## Misconceptions to listen for

- The depth with the highest final accuracy is best in general.
- The final test can be run twice if the first looks bad.
- A small test set gives a precise score.

## Questions to ask, with expected answers

- Which score picks the depth? Expected: The validation score.
- Why report two limitations? Expected: The data is small and the test is only 30 flowers, so the result is uncertain.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
