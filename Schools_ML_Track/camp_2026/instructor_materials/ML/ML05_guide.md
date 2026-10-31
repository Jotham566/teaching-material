# ML05 Instructor guide: Lists, dictionaries and loops

Private. Keep this file out of the student folder.

**Objective.** By the end: you can read a list position and a dictionary key, and trace a loop that adds up values.

**Question of the day.** How do I repeat one calculation for every item in a list?

Prerequisite: ML04 Decisions and a hand-written flower rule.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Lists and dictionaries

A tuck shop keeps three prices in a list and one product in a dictionary.

Ask for the prediction first: Predict what prints. Which number is prices[0]?

```python
prices = [1000, 2000, 3000]
product = {"name": "Juice", "price": 2000}
first = prices[0]
juice_price = product["price"]
print(first)
print(juice_price)
print(len(prices))
```

Correct result: The cell prints 1000, 2000 and 3. Square brackets after a list give the item at that index, and the first index is 0. Square brackets after a dictionary give the value for that key. len counts the items in a list.

Investigate, with answers:

- Why is prices[0] the first price? Answer: Python counts positions from 0.
- What happens if you ask for prices[3]? Answer: An IndexError. The list has positions 0, 1 and 2 only.

Modify: Print the last price using its index. Answer: prices[2] gives 3000.

```python
last = prices[2]
```

## Block B. A loop that adds

Run the loop and follow how total grows after each pass.

Ask for the prediction first: Predict the four numbers printed.

```python
prices = [1000, 2000, 3000]
total = 0
for price in prices:
    print(price * 2)
    total = total + price
print(total)
```

Correct result: The cell prints 2000, 4000, 6000 and then 6000. for price in prices takes one item at a time and runs the indented lines for it. total starts at 0 and grows by the item each pass: 1000, then 3000, then 6000.

Investigate, with answers:

- What is total after the second pass? Answer: 3000, which is 1000 plus 2000.
- What goes wrong if total = 0 is moved inside the loop? Answer: total restarts at 0 on every pass, so only the last item remains.

Modify: Change the list to [1500, 2500] and run the loop again. Answer: The final total is 4000.

```python
prices = [1500, 2500]
total = 0
for price in prices:
    total = total + price
```

## Make: reference

```python
values = [2, 4, 6]
for value in values:
    print(value + 1)
item = {"name": "Book", "stock": 8}
print(item["stock"])
lengths = [1.4, 1.4, 4.7, 4.5, 4.9, 6.0, 5.1, 5.9]
short = 0
for length in lengths:
    if length < 2.5:
        short = short + 1
print(short)
# 3, 5, 7, then 8, then 2 short petals.
```

Evidence to collect: ML05.ipynb with the three loop outputs, the stock 8, and the count 2.

## Misconceptions to listen for

- The first item is at position 1.
- A dictionary keeps its values in a position order.
- A loop changes the original list.

## Questions to ask, with expected answers

- What does position 0 mean? Expected: The first item in the list.
- Where should total = 0 go? Expected: Before the loop, so it starts once.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
