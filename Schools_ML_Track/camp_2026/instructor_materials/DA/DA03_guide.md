# DA03 Instructor guide: Arithmetic, revenue and reading errors

Private. Keep this file out of the student folder.

**Objective.** By the end: you can calculate revenue for a sale, check it by hand, and read an error message to find the line to fix.

**Question of the day.** How much money did the first three sales bring in?

Prerequisite: DA02 Values, names and types.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Students enjoy breaking code on purpose. Keep the deliberate errors in separate cells so working code stays clean.

## Block A. Revenue by hand and by Python

Revenue is units times unit price. The first three sales in the shop table are 1 Book at 3000, 2 Pens at 1000 and 4 Juice at 2000. Work the three revenues out on paper first. A line that starts with # is a comment.

Ask for the prediction first: Predict the three revenues and their total, using paper.

```python
# revenue = units * price
book = 1 * 3000
pen = 2 * 1000
juice = 4 * 2000
total = book + pen + juice
print(book, pen, juice)
print(total)
print(2 + 3 * 4)
print((2 + 3) * 4)
```

Correct result: The cell prints 3000 2000 8000, then 13000, then 14 and 20. Multiplication happens before addition. Brackets change the order.

Investigate, with answers:

- Why does 2 + 3 * 4 give 14 and not 20? Answer: Python multiplies first, so it works out 3 * 4 = 12 and then adds 2. Brackets are needed to add first.
- Why do we say revenue and not profit? Answer: Revenue is the money received. Profit would need the cost of the stock, which the table does not have.

Modify: Change the Pen to 5 units and find the new total. Answer: 16000.

```python
pen = 5 * 1000
total = book + pen + juice
```

## Block B. Reading an error message

An error is feedback about an instruction. It is not a judgement about you. Read the last line first. It names the kind of error. Then find the line number it points to. Type this line in a new cell and run it: print(10 / 0). Then type print(units) in another cell before you have created units.

Ask for the prediction first: Predict the name of each error before you run the lines.

Correct result: The first line stops with ZeroDivisionError: division by zero, because no number answers 10 divided by 0. The second stops with NameError: name 'units' is not defined, because Python has not met a line that creates units. In both cases the last line of the message says what went wrong.

Investigate, with answers:

- Which line of the message do you read first, and why? Answer: The last one. It names the error and says what happened.
- How do you fix a NameError? Answer: Run the cell that creates the name, or correct its spelling and capital letters.

Modify: Fix the NameError by creating units = 4 first and then printing units * 2000. Answer: 8000.

## Make: reference

```python
print(float("12.5") * 4)
# 50.0. No number multiplied by zero gives 10, so 10 divided by 0 has no answer.
```

Evidence to collect: DA03.ipynb with 50.0, the prediction written before the run, and an error log with two errors read correctly.

## Misconceptions to listen for

- An error means the student is bad at this.
- Python reads left to right and ignores bracket rules.
- Revenue and profit are the same.

## Questions to ask, with expected answers

- Why predict before you run? Expected: A prediction shows whether you understand the line. A surprise is where learning happens.
- What does the comment in the code do? Expected: Nothing for Python. It helps the next person read the code.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
