# ML04 Instructor guide: Decisions and a hand-written flower rule

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write an if, elif and else decision, test it at its boundary, and count how often a simple rule is right.

**Question of the day.** How often does a three-line rule name the right flower?

**Where this is used.** Apps decide with rules such as: if the balance is too low, refuse the payment. Botanists also tell flowers apart by measuring petals, and today you write a three-line rule that does it. Can your rule beat a guess?

Prerequisite: ML03 Arithmetic, converting text and reading errors.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: The flower table can overrun. Fill in only the first four flowers together and let students finish the rest in the Make task.

## Block A. A decision with if and else

A student has UGX 10000 and an item costs UGX 8000. Run the cell, then change the cost.

Ask for the prediction first: Predict the message that will print.

```python
budget = 10000
cost = 8000
if cost <= budget:
    message = "Within budget"
else:
    message = "Over budget"
print(message)
```

Correct result: The cell prints Within budget. cost <= budget is a comparison and its answer is True, which is a Boolean. if runs the indented lines when the answer is True and else runs them when it is False. The four spaces at the start of the lines are indentation.

Investigate, with answers:

- What is the answer to 5000 >= 5000? Answer: True. >= means at least.
- What does = do compared with ==? Answer: = stores a value under a name. == asks whether two values are equal.

Modify: Set cost to 12000 and run the decision again. Answer: The message is Over budget.

```python
cost = 12000
if cost <= budget:
    message = "Within budget"
else:
    message = "Over budget"
```

## Block B. A rule that names a flower

The iris data records flowers of three species. Petal length helps tell them apart. Run the rule for one flower, then try the others on the table.

Ask for the prediction first: Look at the rule. Predict which species it names for a petal length of 4.7 centimetres.

```python
petal_length = 4.7
if petal_length < 2.5:
    guess = "setosa"
elif petal_length < 4.8:
    guess = "versicolor"
else:
    guess = "virginica"
print(guess)
```

Correct result: The cell prints versicolor. elif asks a second question only when the first answer was False. Try the eight petal lengths. The true species are setosa twice, versicolor three times and virginica three times. The rule gets seven right and misses the 4.9 flower.

Investigate, with answers:

- Which of the eight flowers does the rule get wrong? Answer: The one with petal length 4.9. It is versicolor, and the rule says virginica.
- How would you move the rule so that 4.9 is right? Answer: Raise the 4.8 limit to 5.0. Then check whether the 5.1 flower is still right.
- What is the accuracy on these eight flowers? Answer: 7 right out of 8, which is 87.5%.

Modify: Set petal_length to 4.9 and run the rule. Answer: It prints virginica, which is wrong for this flower.

```python
petal_length = 4.9
if petal_length < 2.5:
    guess = "setosa"
elif petal_length < 4.8:
    guess = "versicolor"
else:
    guess = "virginica"
```

## Make: reference

```python
budget = 5000
if budget >= 5000:
    decision = "Buy"
else:
    decision = "Save"
print(decision)
# 4999 gives Save; 5000 and 5001 give Buy. The flower rule is right for 7 of 8 flowers.
```

Build log entry to look for: ML04.ipynb with the ticket decision tested at three budgets and the flower count 7 out of 8.

## Misconceptions to listen for

- If a rule is right on a few examples it is right everywhere.
- A single = tests equality.
- The lines after if run even when the answer is False.

## Questions to ask, with expected answers

- Why test 4999, 5000 and 5001? Expected: The change happens at the boundary, and boundaries are where rules break.
- What does the flower rule teach us about prediction? Expected: Even a simple rule is wrong sometimes, so every rule needs counting on examples.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A decision with if and else: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, A rule that names a flower: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A decision with if and else): Set cost to 12000 and run the decision again.
2. Modify, Block B (A rule that names a flower): Set petal_length to 4.9 and run the rule.
3. Make: A ticket costs UGX 5000. Write a decision that prints Buy when the budget is at least 5000 and Save otherwise. Test 4999, 5000 and 5001. Then say how many of the eight flowers your flower rule names correctly.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Why test 4999, 5000 and 5001? Expected: The change happens at the boundary, and boundaries are where rules break.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
