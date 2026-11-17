# ML18 Instructor guide: A fair comparison: does your model beat the plain guess?

Private. Keep this file out of the student folder.

**Objective.** By the end: you can split data into training, validation and held-back parts, choose a model on validation only, and report one held-back result with its limits.

**Question of the day.** Which tree depth is better, and does it beat the plain guess on the held-back flowers?

**Where this is used.** A football coach tests two formations on matches the team has not practised for. You do the same with two tree depths. Would you pick a formation after one lucky match?

Prerequisite: ML17 Mistakes, overfitting and fair comparisons.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | recall |
| 25 | split and plan |
| 15 | break |
| 100 | comparison work |
| 15 | explanation of the decision |
| 15 | save and exit check |

Where it overruns: Keeping the held-back set untouched is the point. Check each learner's order of steps.

## Block A. A three-way split

First hold back 20% of the flowers as the held-back set, then take a quarter of what remains for validation. stratify keeps each species equally represented in every part.

Ask for the prediction first: Predict the three sizes. They should add up to 150.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
X, y = load_iris(return_X_y=True)
X_dev, X_test, y_dev, y_test = train_test_split(X, y, test_size=0.2, random_state=7, stratify=y)
X_train, X_val, y_train, y_val = train_test_split(X_dev, y_dev, test_size=0.25, random_state=7, stratify=y_dev)
print(len(X_train), len(X_val), len(X_test))
```

Correct result: The cell prints 90, 30 and 30. stratify=y means each species has the same share in every part: 10 of each species in validation and in the held-back set. The held-back set is now set aside and must not be used to make any choice.

Investigate, with answers:

- Why are the three parts 60%, 20% and 20%? Answer: 20% is held back first. A quarter of the other 80% is 20% of the total, which leaves 60%.
- What does stratify do that a plain shuffle does not? Answer: It makes sure each part has the same species mix, so a small part is not accidentally missing one.

Modify: Print how many flowers of species 0 are in the validation part. Answer: Ten.

```python
n_setosa_val = int((y_val == 0).sum())
```

## Block B. Choose on validation, test once

Compare a tree of depth 1 and one of depth 3 on validation only. Freeze the winner. Then use the held-back set once.

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

Correct result: The baseline scores exactly one third on validation, because each species is a third. The deeper tree usually wins on validation. The choice is made from the validation scores and then frozen. final_acc is the one honest number: it comes from 30 flowers the choice never saw. The report needs the split sizes, the baseline, both validation scores, the chosen depth, the held-back accuracy, the confusion matrix and two limitations.

Investigate, with answers:

- Which scores did you use to choose the depth? Answer: The validation scores only.
- What is one limitation of a held-back set of 30 flowers? Answer: One flower is more than 3 points of accuracy, so the score is unstable.

Modify: Say what you would do if the held-back score came out lower than the validation score. Answer: Report it as it is. A lower final score is normal, and changing the choice now would use the held-back set twice.

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

Build log entry to look for: ML18.ipynb: split sizes 90, 30 and 30, baseline, two validation scores, the chosen depth, one held-back accuracy, a confusion matrix and two limitations.

## Misconceptions to listen for

- The depth with the highest held-back accuracy is best in general.
- The held-back set can be used twice if the first result looks bad.
- A small test set gives a precise score.

## Questions to ask, with expected answers

- Which score picks the depth? Expected: The validation score.
- Why report two limitations? Expected: The data is small and the test is only 30 flowers, so the result is uncertain.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A three-way split: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Choose on validation, test once: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A three-way split): Print how many flowers of species 0 are in the validation part.
2. Modify, Block B (Choose on validation, test once): Say what you would do if the held-back score came out lower than the validation score.
3. Make: Save ML18.ipynb with: the split sizes, the baseline, two validation scores, the chosen depth, the held-back accuracy, the confusion matrix and two limitations. Explain your decision without claiming that the highest score proves one depth is best in general.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Which score picks the depth? Expected: The validation score.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
