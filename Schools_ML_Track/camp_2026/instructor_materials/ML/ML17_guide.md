# ML17 Instructor guide: Mistakes, overfitting and fair comparisons

Private. Keep this file out of the student folder.

**Objective.** By the end: you can read a confusion matrix, spot an overfitted tree from its training and test scores, and explain why the final test must stay locked.

**Question of the day.** When is a very high score a warning sign?

Prerequisite: ML16 Predicting a category with a decision tree.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Read a confusion matrix

A model guessed five yes or no answers. Count the matches.

Ask for the prediction first: The matrix will have two rows and two columns. Predict which cells hold the correct answers.

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
actual = [0, 0, 1, 1, 1]
predicted = [0, 1, 1, 0, 1]
matrix = confusion_matrix(actual, predicted, labels=[0, 1])
print(matrix)
ConfusionMatrixDisplay(matrix, display_labels=["no", "yes"]).plot()
plt.show()
```

Correct result: The cell prints [[1 1] [1 2]]. Rows are the actual answers and columns are the predicted answers. The top-left cell is an actual no predicted no, and the bottom-right is an actual yes predicted yes. The correct answers are on the diagonal: 1 plus 2 is 3 out of 5. ConfusionMatrixDisplay draws the table as a picture.

Investigate, with answers:

- Which cell counts an actual yes that the model called no? Answer: The bottom-left cell. It holds 1.
- Why read the axis labels before the numbers? Answer: If you mix up rows and columns you will swap the two kinds of mistake.

Modify: Calculate the accuracy from the matrix. Answer: 3 divided by 5 is 0.6, or 60%.

```python
accuracy = (matrix[0, 0] + matrix[1, 1]) / matrix.sum()
```

## Block B. The tree that remembered

Train trees that may ask more and more questions, and print their training and test scores.

Ask for the prediction first: Predict which tree scores 100% on the training flowers.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.25, random_state=7)
for depth in [1, 2, 3, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=7).fit(X_train, y_train)
    print(depth, round(model.score(X_train, y_train), 3), round(model.score(X_test, y_test), 3))
gap = model.score(X_train, y_train) - model.score(X_test, y_test)
```

Correct result: Each line prints the depth, the training score and the test score. The tree with depth None may ask as many questions as it likes and scores 1.0 on the training flowers, because it memorised them. Its test score does not rise with it. That gap between training and test is the sign of overfitting. score gives the accuracy.

Investigate, with answers:

- Why is 100% on training flowers a warning sign? Answer: The tree may have memorised the flowers. Only the test score says how it does on new ones.
- Can we use the test score to pick the best depth? Answer: No. A choice made by looking at test scores uses the test as a practice exam, and the final test then proves nothing.

Modify: Print the gap between the last tree's training and test scores. Answer: The gap is the training score minus the test score; it is zero or more.

```python
gap2 = model.score(X_train, y_train) - model.score(X_test, y_test)
```

## Make: reference

```python
from sklearn.metrics import confusion_matrix
matrix = confusion_matrix([0, 0, 1, 1, 1], [0, 1, 1, 0, 1], labels=[0, 1])
right = matrix[0, 0] + matrix[1, 1]
wrong = matrix.sum() - right
print(right, wrong)
# 3 right, 2 wrong. If you tune against the final test, it has become a validation set and a new test is needed.
```

Evidence to collect: ML17.ipynb with the labelled matrix, 3 right and 2 wrong, and the explanation about tuning on the test.

## Misconceptions to listen for

- A higher training score always means a better model.
- I can try settings on the final test until I like the result.
- A small test set gives stable scores.

## Questions to ask, with expected answers

- What does the diagonal of a confusion matrix hold? Expected: The correct predictions.
- What changes if you choose a depth by looking at test scores? Expected: The test is no longer unseen, so it cannot give an honest final score.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
