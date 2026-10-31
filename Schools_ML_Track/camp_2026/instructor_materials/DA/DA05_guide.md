# DA05 Instructor guide: Lists, dictionaries and loops

Private. Keep this file out of the student folder.

**Objective.** By the end: you can store several values in a list, look one up by position, and use a loop to add them up.

**Question of the day.** How many units did the first six sales sell in total?

Prerequisite: DA04 Conditions and decisions.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Lists and positions

The units of the first six sales in the shop table are 1, 2, 4, 7, 6 and 5. A list keeps them in order inside square brackets. Square brackets after a list name pick out one position. Position 0 is the first.

Ask for the prediction first: Predict what each print shows.

```python
units = [1, 2, 4, 7, 6, 5]
print(units[0])
print(units[3])
print(len(units))
print(max(units))
```

Correct result: The cell prints 1, 7, 6 and 7. Position 0 holds the first value and position 3 holds the fourth. len counts the values and max finds the largest.

Investigate, with answers:

- Why does units[3] show 7 and not 4? Answer: Counting starts at 0, so position 3 is the fourth value.
- Which position holds the last value? Answer: Position 5, which is len(units) - 1.

Modify: Print the value at position 4. Answer: 6.

```python
fifth = units[4]
```

## Block B. Dictionaries and a loop with a running total

A dictionary stores named pairs. A for loop repeats its indented lines for each value in a list. The name after for stands for the current value.

Ask for the prediction first: Predict the final total and the price of Pen.

```python
units = [1, 2, 4, 7, 6, 5]
prices = {"Book": 3000, "Pen": 1000, "Juice": 2000}
print(prices["Pen"])
total_units = 0
for u in units:
    total_units = total_units + u
print(total_units)
```

Correct result: The cell prints 1000 and then 25. The loop starts the running total at 0 and adds each of the six values in turn: 1, 3, 7, 14, 20, 25.

Investigate, with answers:

- What does the line total_units = total_units + u do? Answer: It reads the current total, adds u and stores the answer back under the same name.
- What would happen if total_units = 0 sat inside the loop? Answer: The total would restart for each value and end as the last value only, which is 5.

Modify: Change the loop to print each value plus 1 and then print the final total. Answer: The loop prints 2, 3, 5, 8, 7, 6.

```python
plus_one = []
for u in units:
    plus_one.append(u + 1)
```

## Make: reference

```python
values = [2, 4, 6]
for v in values:
    print(v + 1)
item = {"name": "Book", "stock": 8}
print(item["stock"])
# 3, 5, 7 and then 8.
```

Evidence to collect: DA05.ipynb with the loop output 3, 5, 7, the stock 8 and the explanation of position 0.

## Misconceptions to listen for

- The first value is at position 1.
- The loop variable keeps its old value when the loop ends.
- A dictionary has an order like a list.

## Questions to ask, with expected answers

- How many values does a list of six have, and what is the last index? Expected: Six values. The last index is 5.
- Why does the running total start at zero? Expected: Nothing has been added yet.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
