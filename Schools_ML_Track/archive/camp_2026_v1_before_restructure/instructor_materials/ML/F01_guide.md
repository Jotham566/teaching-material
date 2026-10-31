# F01 Numbers, names and predicting Python output

Week 1, fourth teaching day. Complete ML03 first.

## Learn the idea

A number represents a quantity. A whole number such as 3 is an integer; 2.5 is a decimal (a float in Python). A variable is a name referring to a value, like a labelled box. Python reads instructions from top to bottom. The equals sign stores a value under a name; it does not ask a question. A string is text surrounded by quotes. Multiplication uses * and division uses /. Parentheses control which calculation happens first. print(...) displays its input. Indented lines are not needed for these simple instructions.

## Start on paper

Draw three pens. Label each UGX 1,000. Add the prices by hand: 1,000 + 1,000 + 1,000 = 3,000. Explain why 3 * 1000 gives the same total. Predict every printed line before running the code.

## Worked example

```python
units = 3
price = 1000
total = units * price
print(total)
print(total / units)
print("1000")
units = 4
print(total)
total = units * price
print(total)
```

Expected output: 3000, 1000.0, 1000, 3000, 4000 on separate lines. The quoted 1000 is text. Updating units alone does not rerun an earlier calculation.

## Your turn

In a new code cell calculate the price of 5 books at UGX 3,000 each. Print the total. Change the quantity to 2 and recalculate. Add a text cell explaining why the old total did not change until you recalculated it. Save F01.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation. Use the private submission route in START_HERE.md if a hand-in is requested.

## Tutor pacing and explanations

10 minutes recall; 20 minutes paper example; 20 minutes slowly run the code; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120 minutes. Visit all five learners. Ask what each symbol and unit means before asking them to change it.

Reference: 15000 then 6000; assignments execute when run, not continuously. Require the learner to point to the changed input and rerun from the first cell.

Repair: If quotes surround a quantity, remove them to make it numeric. If the total is stale, rerun the calculation after changing the input. Do not move on until the learner can predict both totals.

Record complete / needs repair / absent. Carry unfinished repair into the next core session; defer its optional extension to protect foundation learning. Include this evidence in the existing week’s portfolio, without adding a second mark or increasing the assessment weight.
