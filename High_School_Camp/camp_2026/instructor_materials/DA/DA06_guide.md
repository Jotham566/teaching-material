# DA06 Instructor guide: Functions and checks that fail loudly

Private. Keep this file out of the student folder.

**Objective.** By the end: you can write a function that returns a result, and use assert to check it on known cases.

**Question of the day.** Can we trust our revenue calculation on cases we already know the answer to?

**Where this is used.** Payment and tax software relies on functions that must give the right answer on cases where the answer is already known. A check that fails loudly protects every customer. What known case would you use to test a discount function?

Prerequisite: DA05 Lists, dictionaries and loops.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: Students often confuse the definition with a call. Run the def cell, show nothing happens, then call it.

## Block A. A function and a check

A function starts with def. print only shows something on the screen. return sends a result back so other code can use it. A passing assert prints nothing at all. A failing one stops with an error.

Ask for the prediction first: Predict what the function returns for 3 units at 2000 shillings, and what a passing assert prints.

```python
def revenue(units, price):
    return units * price

print(revenue(3, 2000))
assert revenue(3, 2000) == 6000
assert revenue(0, 2000) == 0
```

Correct result: The cell prints 6000. The two asserts print nothing, which means both pass. units and price are the parameters. 3 and 2000 are the arguments.

Investigate, with answers:

- What is the difference between return and print? Answer: return gives the value to the rest of the program. print only shows it.
- What does it mean that the asserts print nothing? Answer: The statements are True. Silence means the check passed.

Modify: Add a third assert that checks revenue(5, 1000) equals 5000. Answer: It passes silently.

```python
assert revenue(5, 1000) == 5000
```

## Block B. Edge cases and a guard

A share is a part divided by a whole. Dividing by zero is an edge case. A function can guard against it with an if before it divides.

Ask for the prediction first: Predict the result of share(12, 20) and of share(5, 0).

```python
def share(part, whole):
    if whole == 0:
        return 0
    return part / whole

print(share(12, 20))
print(share(5, 0))
assert share(12, 20) == 0.6
assert share(5, 0) == 0
```

Correct result: The cell prints 0.6 and then 0. When the whole is zero the function returns before it divides, so no error appears.

Investigate, with answers:

- Why does the function check the whole before it divides? Answer: Dividing by zero stops the program with an error. The check avoids it.
- Is returning 0 for share(5, 0) always the right answer? Answer: Not always. It is a choice that must be stated, because a share of nothing is undefined.

Modify: Add an assert that share(1, 4) equals 0.25. Answer: It passes silently.

```python
assert share(1, 4) == 0.25
```

## Make: reference

```python
def price_after_discount(price, percent):
    return price * (100 - percent) / 100
assert price_after_discount(2000, 0) == 2000
assert price_after_discount(2000, 10) == 1800
assert price_after_discount(2000, 100) == 0
```

Build log entry to look for: DA06.ipynb with the function and three passing asserts, rerun from the top.

## Misconceptions to listen for

- print and return do the same thing.
- Defining a function runs it.
- A silent assert means nothing happened.

## Questions to ask, with expected answers

- Which three inputs do you test for a discount function? Expected: Zero percent, an ordinary percent and 100 percent, which are the edges and a middle case.
- Why use assert when we can read the output ourselves? Expected: The computer checks every time, and a wrong answer stops the program loudly.

## Online version

For a hybrid group. The live class is 90 minutes on video with screen sharing. The learner finishes the build in their own time, about an hour. The full rules are in handbook/HYBRID_DELIVERY.md.

### Live clock, 90 minutes

| Minutes | Activity |
|---|---|
| 5 | Recall: three questions on paper, then say the answers aloud |
| 35 | Block A, A function and a check: predict, run, investigate. The Modify step moves to the build task. |
| 5 | Break away from the screen |
| 35 | Block B, Edge cases and a guard: predict, run, investigate. The Modify step moves to the build task. |
| 10 | Close: say the exit sentence aloud, then the build task is set |

### After-class build task, about an hour

1. Modify, Block A (A function and a check): Add a third assert that checks revenue(5, 1000) equals 5000.
2. Modify, Block B (Edge cases and a guard): Add an assert that share(1, 4) equals 0.25.
3. Make: Write price_after_discount(price, percent) that returns the price after a percentage discount. Check it with assert for 0 percent, 10 percent and 100 percent on a price of 2000. Save the notebook and run all cells from the top.

When you finish, write two sentences: what you changed and how you checked it. Add a build log entry. Send a photo of your work or the notebook by the route the organiser sets, before the next class.

### Next class

In the next class recall, ask: Which three inputs do you test for a discount function? Expected: Zero percent, an ordinary percent and 100 percent, which are the edges and a middle case.

## Build log and feedback

Look at what each of the five learners saved and note one strength and one next step for each. Share them kindly and privately. Nothing is scored or ranked. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and show-and-tells need your judgement.
