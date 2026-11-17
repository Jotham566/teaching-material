# ML06 Instructor guide: Functions and checks that fail loudly

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write a function that returns a result, and check it against known answers with assert.

**Question of the day.** How do I turn my flower rule into a reusable tool and test it?

**Where this is used.** A fee calculator is a function: write it once and use it for every payment. Software teams also write checks with known answers, so a mistake shows up before a customer finds it. What check would you write for a fee calculator?

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

Build log entry to look for: ML06.ipynb with double defined, three passing asserts, and a clean run from the top.

## Misconceptions to listen for

- Defining a function runs it.
- print and return do the same job.
- A passing assert should show a message.

## Questions to ask, with expected answers

- What makes a good test case? Expected: A case where you already know the right answer, including a boundary such as 0.
- What does assert print when it passes? Expected: Nothing.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A function and an assert: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, The flower rule as a function: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A function and an assert): Add an assert that total(1000, 0) equals 0.
2. Modify, Block B (The flower rule as a function): Add the flower [4.9, "versicolor"] again to the list and recount.
3. Make: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2) with assert. Save the notebook and run all cells from the top.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: What makes a good test case? Expected: A case where you already know the right answer, including a boundary such as 0.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
