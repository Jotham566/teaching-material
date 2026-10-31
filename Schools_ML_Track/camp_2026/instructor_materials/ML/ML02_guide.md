# ML02 Instructor guide: Values, names and types

Private. Keep this file out of the student folder.

**Objective.** By the end: you can create whole numbers, decimals and text, and predict what happens when a name is given a new value.

**Question of the day.** What kind of thing is each part of a sale?

Prerequisite: ML01 Your first instruction and your first prediction.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Names point to values

A shop sells 3 items at UGX 2000 each. Run the cell and read each line of output.

Ask for the prediction first: Predict the three lines the cell will print.

```python
price = 2000
quantity = 3
cost = price * quantity
print(cost)
print(type(price))
print(type("2000"))
```

Correct result: The cell prints 6000, then <class 'int'>, then <class 'str'>. price and quantity are variables. 2000 is an integer. The quoted 2000 is a string, which is text. The equals sign stores the value on its right under the name on its left.

Investigate, with answers:

- Why is type("2000") a string? Answer: Quotation marks make it text. Python cannot multiply it like an amount of money.
- What does the equals sign do in cost = price * quantity? Answer: It calculates the right side first, then stores the answer under the name cost.

Modify: Change quantity to 5 and run the whole cell again. Answer: cost becomes 10000.

```python
quantity = 5
cost = price * quantity
```

## Block B. A name keeps its value until you change it

Run the cell and watch what the printed total does when quantity changes.

Ask for the prediction first: Predict the three numbers printed. Will the second one change after quantity changes?

```python
price = 2500.5
quantity = 2
total = price * quantity
print(total)
quantity = 4
print(total)
total = price * quantity
print(total)
```

Correct result: The cell prints 5001.0, then 5001.0, then 10002.0. 2500.5 is a float. Changing quantity does not change total until the line that calculates total runs again. Python works from the top of the cell to the bottom.

Investigate, with answers:

- Why does the second print still show 5001.0? Answer: total was calculated when quantity was 2. Python does not recalculate by itself.
- What line makes the third number different? Answer: The second total = price * quantity line, which runs with quantity equal to 4.

Modify: Set quantity to 10, recalculate total and print it. Answer: The total is 25005.0.

```python
quantity = 10
total = price * quantity
```

## Make: reference

```python
price = 2500.5
quantity = 2
print(price * quantity)
print(type("2500.5"))
# 5001.0. With quotation marks 2500.5 is a string, which is text and not an amount.
```

Evidence to collect: ML02.ipynb with the total 5001.0 and a sentence explaining the quotation marks.

## Misconceptions to listen for

- = asks whether two things are equal.
- Quotation marks around a number change nothing.
- Changing quantity changes total automatically.

## Questions to ask, with expected answers

- What does the equals sign do? Expected: It stores the value on the right under the name on the left.
- Why is 5001.0 shown with a decimal point? Expected: Multiplying by a float gives a float.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
