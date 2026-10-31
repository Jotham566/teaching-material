# ML06 Instructor guide: Functions and checks that fail loudly

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write a function that returns a result, and check it against known answers with assert.

**Question of the day.** How do I turn my flower rule into a reusable tool and test it?

Prerequisite: ML05 Lists, dictionaries and loops.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. A function and an assert

A function names a calculation so you can use it again. Run the cell. A passing assert prints nothing.

Ask for the prediction first: Predict what total(2000, 3) gives and what happens when the assert passes.

```python
def total(price, quantity):
    return price * quantity

result = total(2000, 3)
print(result)
assert total(2000, 3) == 6000
```

Correct result: The cell prints 6000. def starts the function. price and quantity are parameters, and the 2000 and 3 you give it are arguments. return sends the answer back. assert stops with an error when the statement is false, and a passing assert prints nothing.

Investigate, with answers:

- What is the difference between return and print? Answer: return gives the value back to the program. print only shows it on the screen.
- What happens if you define total but never call it? Answer: Nothing runs. Defining a function does not run its lines.

Modify: Add an assert that total(1000, 0) equals 0. Answer: It passes silently, because 1000 times 0 is 0.

```python
assert total(1000, 0) == 0
```

## Block B. The flower rule as a function

Your rule from session 4 becomes a function. Three asserts test it, and a loop counts it on eight flowers.

Ask for the prediction first: Predict how many of the eight flowers the function names correctly.

```python
def guess_species(petal_length):
    if petal_length < 2.5:
        return "setosa"
    elif petal_length < 4.8:
        return "versicolor"
    else:
        return "virginica"

assert guess_species(1.4) == "setosa"
assert guess_species(4.7) == "versicolor"
assert guess_species(6.0) == "virginica"
flowers = [[1.4, "setosa"], [1.4, "setosa"], [4.7, "versicolor"], [4.5, "versicolor"], [4.9, "versicolor"], [6.0, "virginica"], [5.1, "virginica"], [5.9, "virginica"]]
right = 0
for flower in flowers:
    if guess_species(flower[0]) == flower[1]:
        right = right + 1
print(right)
```

Correct result: The cell prints 7. The three asserts pass without a sound. Each flower in the list holds a petal length at position 0 and a species at position 1. The function is right for seven of eight flowers, the same count you found by hand.

Investigate, with answers:

- What does flower[0] give? Answer: The petal length, because position 0 is the first item.
- Why test the function on three known flowers before counting? Answer: If an assert fails you know the rule is broken before you trust any count.

Modify: Add the flower [4.9, "versicolor"] again to the list and recount. Answer: The count becomes 7 out of 9, because the 4.9 flower is wrong each time.

```python
flowers = flowers + [[4.9, "versicolor"]]
right = 0
for flower in flowers:
    if guess_species(flower[0]) == flower[1]:
        right = right + 1
```

## Make: reference

```python
def double(number):
    return number * 2

assert double(4) == 8
assert double(0) == 0
assert double(-2) == -4
```

Evidence to collect: ML06.ipynb with double defined, three passing asserts, and a clean run from the top.

## Misconceptions to listen for

- Defining a function runs it.
- print and return do the same job.
- A passing assert should show a message.

## Questions to ask, with expected answers

- What makes a good test case? Expected: A case where you already know the right answer, including a boundary such as 0.
- What does assert print when it passes? Expected: Nothing.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
