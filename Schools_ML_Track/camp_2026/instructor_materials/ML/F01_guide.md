# F01 Numbers, names and predicting Python output

Week 1, fourth teaching day. Complete ML03 first.

**Today's question.** Can I predict every line Python prints before I run it?

## Words for today

| Word | What it means | Think of it like this |
|---|---|---|
| scalar | One number. | One price on a label. |
| name | A label that points to a value. | A tag on a box. |
| top to bottom | Python reads one line after another and does not look ahead. | Reading a recipe in order. |
| update | Giving an existing name a new value. | Crossing out a price and writing a new one. |
| string | Text inside quotation marks. | A word on a label. |
| prediction on paper | Writing what you expect before you run. | Guessing the match score before kick-off. |

## Learn the idea

Python reads instructions from the top to the bottom, one at a time. A name points to a value. Changing a name does not change a result that was already calculated. Multiplication uses * and division uses /. The text in quotation marks is a string even when it looks like a number. print shows its input.

## Start on paper

Draw three pens and label each UGX 1,000. Add them by hand: 1,000 + 1,000 + 1,000 is 3,000. Explain why 3 * 1000 gives the same total. Then write on paper every line the code below will print, before you run it.

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

Run it, then compare: 3000, 1000.0, 1000, 3000 and 4000, on separate lines. The quoted 1000 is text. Changing units alone does not recalculate an earlier total.

## Your turn

In a new code cell calculate the price of 5 books at UGX 3000 each and print it. Change the quantity to 2 and recalculate. In a text cell explain why the old total did not change until you recalculated it. Save F01.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation.

## Tutor pacing

10 minutes recall; 20 minutes paper example; 20 minutes run the code slowly together; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120. Visit all five learners and ask what each symbol and unit means before asking them to change it.

Reference: 15000, then 6000. A calculation runs when its line runs and it does not update by itself. Ask the learner to point to the changed input and rerun from the first cell.

Repair: If quotation marks surround a quantity, remove them so it is a number. If a total looks stale, rerun the line that calculates it. Do not move on until the learner can predict both totals.

Record complete, needs repair or absent. Carry unfinished repair into the next core session. Lab evidence goes in that week's portfolio with no second mark.
