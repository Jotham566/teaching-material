# ML16 Instructor guide: Predicting a category with a decision tree

Private. Keep this file out of the student folder.

**Objective.** By the end: you can train a small decision tree on iris, read its first question, and compare its accuracy with a baseline and with the hand rule from session 4.

**Question of the day.** Does a tree that learned its questions beat my hand-written flower rule?

Prerequisite: ML15 A complete regression experiment.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Train a tree and draw it

Split the 150 iris flowers, train a tree that may ask two questions in a row, and draw it.

Ask for the prediction first: Predict whether the tree's accuracy will be above 85% and whether the majority baseline will be above 55%.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.25, random_state=7)
tree = DecisionTreeClassifier(max_depth=2, random_state=7).fit(X_train, y_train)
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
tree_acc = accuracy_score(y_test, tree.predict(X_test))
base_acc = accuracy_score(y_test, baseline.predict(X_test))
print(round(tree_acc, 3), round(base_acc, 3))
plot_tree(tree, feature_names=iris.feature_names, class_names=list(iris.target_names))
plt.show()
```

Correct result: The tree scores above 0.85 and the majority baseline scores about a third, because the three species are equally common. plot_tree draws the questions: the top box asks about a petal measurement, the same kind of question as your hand rule. The classes are coded 0, 1 and 2 for setosa, versicolor and virginica. The codes name categories, so species 2 is not twice species 1. Accuracy is correct predictions divided by all predictions.

Investigate, with answers:

- What does the top box of the drawn tree ask? Answer: A yes or no question about a petal measurement. Read it aloud.
- Why does the baseline score near one third? Answer: Each species has about a third of the flowers, so always naming one is right about a third of the time.
- Why is species code 2 not twice species code 1? Answer: The codes are labels. They carry no amounts.

Modify: Change max_depth to 1 and run again. Answer: The tree has one question and scores lower, about two thirds.

```python
tree1 = DecisionTreeClassifier(max_depth=1, random_state=7).fit(X_train, y_train)
acc1 = accuracy_score(y_test, tree1.predict(X_test))
```

## Block B. Back to the hand rule

Score your session 4 rule on all 150 flowers. Petal length is column 2 of the data. The rule says setosa below 2.5, versicolor below 4.8 and virginica otherwise.

Ask for the prediction first: Predict whether your hand rule will score above or below the tree.

```python
lengths = iris.data[:, 2]
guess = (lengths >= 2.5).astype(int) + (lengths >= 4.8).astype(int)
hand_acc = (guess == iris.target).mean()
print(round(hand_acc, 3))
```

Correct result: The hand rule scores above 0.9 on all 150 flowers. Each comparison gives True or False for every flower and astype(int) turns them into 1 and 0. Adding the two gives 0 for setosa, 1 for versicolor and 2 for virginica. Your rule and the tree use the same idea. The tree chose its question and cut-off by itself, and you chose yours by looking at eight flowers.

Investigate, with answers:

- Why does the hand rule use only petal length? Answer: That was the one measurement you looked at. The tree may use any of the four.
- Whose score is fairer: the hand rule on all 150 flowers, or the tree on the 38 held-out flowers of a 112 and 38 split? Answer: Neither is exactly fair. Your rule was designed with a few of these flowers in view, and the tree's test set is small.

Modify: Change 4.8 to 5.0 in the rule and score it again. Answer: The score changes a little. Check whether it rises or falls.

```python
guess5 = (lengths >= 2.5).astype(int) + (lengths >= 5.0).astype(int)
acc5 = (guess5 == iris.target).mean()
```

## Make: reference

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.25, random_state=7)
tree = DecisionTreeClassifier(max_depth=2, random_state=7).fit(X_train, y_train)
percent = accuracy_score(y_test, tree.predict(X_test)) * 100
print(round(percent, 1))
# Target: species. One input: petal length. The codes are labels that carry no amounts.
```

Evidence to collect: ML16.ipynb with both accuracies as percentages, the target and one input named, and the sentence about codes.

## Misconceptions to listen for

- Species code 2 is twice species code 1.
- A tree always beats a hand-written rule.
- An accuracy of 100% on training flowers means the tree is perfect.

## Questions to ask, with expected answers

- What does max_depth limit? Expected: How many questions in a row the tree may ask.
- Why print the baseline accuracy? Expected: To show how much better than guessing the tree is.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
