# ML03 Instructor guide: Arithmetic, converting text and reading errors

Private. Keep this file out of the student folder.

**Objective.** By the end: you can calculate with the five basic operators, turn text into a number, and find the line an error points to.

**Question of the day.** How do I turn the text of a price into a number I can calculate with?

Prerequisite: ML02 Values, names and types.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Students spend longest on reading errors. Cut the extra operator practice before cutting the error routine.

## Block A. The basic operators

Run the cell. Notice the difference the brackets make.

Ask for the prediction first: Predict the four numbers before you run.

```python
price = 3000
total = price * 4
share = price / 4
no_brackets = price - 500 * 2
with_brackets = (price - 500) * 2
print(total, share, no_brackets, with_brackets)
```

Correct result: The cell prints 12000, 750.0, 2000 and 5000. + adds, - subtracts, * multiplies and / divides. Multiplication happens before subtraction, so the brackets change the answer from 2000 to 5000. Brackets are called parentheses.

Investigate, with answers:

- Why do 2000 and 5000 differ? Answer: Without brackets 500 * 2 happens first. With brackets 3000 - 500 happens first.
- Why is share 750.0 and not 750? Answer: Division always gives a float in Python.

Modify: Write the calculation for 3 books at UGX 3000 plus 2 pens at UGX 1000 in one line. Answer: 3 * 3000 + 2 * 1000 gives 11000.

```python
basket = 3 * 3000 + 2 * 1000
```

## Block B. Text becomes a number

A price arrives as text from a form. Run the cell and read the result.

Ask for the prediction first: Predict the output. Can Python multiply text by 4 and give 50.0?

```python
# The price came in as text
text_price = "12.5"
price = float(text_price)
total = price * 4
print(total)
```

Correct result: The cell prints 50.0. float turns the text 12.5 into a number. The line starting with # is a comment, which Python ignores. If the text were abc, float would stop with a ValueError and the last line of the error would name the problem.

Investigate, with answers:

- Which line of an error message do you read first? Answer: The last line. It names the kind of error and what went wrong.
- What does float("12,5") do? Answer: It stops with a ValueError, because Python does not accept a comma inside a number.

Modify: Change the text price to "20" and run the cell again. Answer: The total becomes 80.0.

```python
text_price = "20"
price = float(text_price)
total = price * 4
```

## Make: reference

```python
cost_of_four = float("12.5") * 4
print(cost_of_four)
# 50.0. Dividing by zero asks how many times zero fits into a number, and there is no answer.
```

Evidence to collect: ML03.ipynb with the prediction written first, the result 50.0, and a sentence on division by zero.

## Misconceptions to listen for

- Brackets are decoration.
- An error is a judgement about me.
- Text that looks like a number can be multiplied.

## Questions to ask, with expected answers

- What is the difference between 12.5 and "12.5"? Expected: The first is a number. The second is text.
- Where do you start reading an error? Expected: At the last line, then the line number it names.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
