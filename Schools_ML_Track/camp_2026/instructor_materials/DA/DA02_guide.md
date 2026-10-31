# DA02 Instructor guide: Values, names and types

Private. Keep this file out of the student folder.

**Objective.** By the end: you can store numbers and text under names, and say what type each one is.

**Question of the day.** What kind of thing is each part of a sale?

Prerequisite: DA01 Open a notebook and read your first table.

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

A shop sells 3 Juice bottles at 2000 shillings each. The equals sign stores a value under a name. The right side is worked out first.

Ask for the prediction first: Predict the three lines the cell will print.

```python
price = 2000
units = 3
revenue = price * units
print(revenue)
print(type(price))
print(type("2000"))
```

Correct result: The cell prints 6000, then <class 'int'>, then <class 'str'>. price and units are variables. 2000 is an integer. The quoted "2000" is a string, which is text. The equals sign stores the value on its right under the name on its left.

Investigate, with answers:

- Why is type("2000") a string? Answer: Quotation marks make it text. Python cannot multiply it like an amount of money.
- What does the equals sign do in revenue = price * units? Answer: It works out the right side first and then stores the answer under the name revenue.

Modify: Change units to 5 and run the whole cell again. Answer: revenue becomes 10000.

```python
units = 5
revenue = price * units
```

## Block B. Decimals and converting text

Prices can have decimals. Text that looks like a number has to be converted before Python can calculate with it. The words float and int convert text into those types.

Ask for the prediction first: Predict what each of the first three prints shows, and whether the last line will work.

```python
price = 2500.5
text_price = "2500.5"
print(type(price))
print(type(text_price))
print(price * 2)
print(float(text_price) * 2)
```

Correct result: The cell prints <class 'float'>, <class 'str'>, 5001.0 and 5001.0. The quoted price is text. float() turns it into a number that can be multiplied.

Investigate, with answers:

- Why does the answer 5001.0 keep a decimal point even though 2 is a whole number? Answer: Multiplying a float by 2 gives a float. Python keeps the decimal point.
- What would happen with float("two")? Answer: An error. Only text that looks like a number can be converted.

Modify: Convert the text "1500" to an integer with int() and multiply it by 4. Answer: 6000.

```python
total = int("1500") * 4
```

## Make: reference

```python
price = 2500.5
quantity = 2
print(price * quantity)
print(type("2500.5"))
# 5001.0. With quotation marks 2500.5 is a string, which is text and not an amount.
```

Evidence to collect: DA02.ipynb with the total 5001.0 and a sentence about the quotation marks.

## Misconceptions to listen for

- The equals sign asks whether two things are equal.
- Quotation marks around a number change nothing.
- Changing units changes revenue automatically.

## Questions to ask, with expected answers

- What does the equals sign do? Expected: It stores the value on the right under the name on the left.
- Why is 5001.0 shown with a decimal point? Expected: Multiplying by a float gives a float.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
