# ML04 Instructor guide: Decisions and a hand-written flower rule

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write an if, elif and else decision, test it at its boundary, and count how often a simple rule is right.

**Question of the day.** How often does a three-line rule name the right flower?

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

Evidence to collect: ML04.ipynb with the ticket decision tested at three budgets and the flower count 7 out of 8.

## Misconceptions to listen for

- If a rule is right on a few examples it is right everywhere.
- A single = tests equality.
- The lines after if run even when the answer is False.

## Questions to ask, with expected answers

- Why test 4999, 5000 and 5001? Expected: The change happens at the boundary, and boundaries are where rules break.
- What does the flower rule teach us about prediction? Expected: Even a simple rule is wrong sometimes, so every rule needs counting on examples.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
