# DA04 Instructor guide: Conditions and decisions

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write a decision that gives a different answer for True and False, and test it at the edge.

**Question of the day.** Is this sale big enough to count as a large order?

Prerequisite: DA03 Arithmetic, revenue and reading errors.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Compare and decide

A comparison asks a question. == asks whether two values are equal. >= means at least. The word if runs its indented lines only when the answer is True. A colon ends the if line and four spaces mark the lines that belong to it.

Ask for the prediction first: Predict what prints for a budget of 4999, then for 5000, then for 5001.

```python
budget = 5000
print(budget >= 5000)
if budget >= 5000:
    print("Buy")
else:
    print("Save")
```

Correct result: The cell prints True and then Buy. With a budget of 4999 the comparison is False and the cell prints Save. 5000 and 5001 both print Buy, because >= includes the edge value.

Investigate, with answers:

- Why does 5000 print Buy? Answer: >= means greater than or equal to, so the edge value passes.
- What is the difference between = and ==? Answer: = stores a value under a name. == asks whether two values are equal.

Modify: Set budget to 4999 and run the cell again. Answer: It prints Save.

```python
budget = 4999
result = "Buy" if budget >= 5000 else "Save"
```

## Block B. Two conditions together

A large order needs 5 units or more. An expensive item costs 2000 shillings or more. and needs both to be True. or needs at least one.

Ask for the prediction first: Predict the answer for 6 units of an item at 1000 shillings, for both rules.

```python
units = 6
price = 1000
large = units >= 5
expensive = price >= 2000
print(large and expensive)
print(large or expensive)
if large and expensive:
    print("Large and expensive")
elif large:
    print("Large only")
else:
    print("Small")
```

Correct result: The cell prints False, then True, then Large only. The order is large and not expensive, so and gives False and or gives True. elif means else if: it tests a second condition when the first is False.

Investigate, with answers:

- Why is the answer to large and expensive False? Answer: and needs both conditions True. The price is 1000, which is under 2000.
- Which branch runs for 3 units at 2500 shillings? Answer: Neither if nor elif, so else runs and it prints Small.

Modify: Change the price to 2500 and run the cell again. Answer: It prints Large and expensive.

```python
price = 2500
expensive = price >= 2000
both = large and expensive
```

## Make: reference

```python
def decide(budget):
    if budget >= 5000:
        return "Buy"
    else:
        return "Save"
print(decide(4999), decide(5000), decide(5001))
# Save Buy Buy
```

Evidence to collect: DA04.ipynb with the decision tested at 4999, 5000 and 5001.

## Misconceptions to listen for

- = and == are the same.
- The indentation is only for looks.
- or means exactly one of the two.

## Questions to ask, with expected answers

- Which three values do you test for a rule that says at least 5000? Expected: 4999, 5000 and 5001: just below, on and just above the edge.
- What happens to the else lines when the condition is True? Expected: They are skipped.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
