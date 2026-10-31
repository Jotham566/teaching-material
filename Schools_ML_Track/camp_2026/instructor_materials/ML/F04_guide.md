# F04 Matrices, weighted sums and slope

Week 4, fourth teaching day. Complete ML12 first.

**Today's question.** How does a model turn two measurements into one prediction?

## Words for today

| Word | What it means | Think of it like this |
|---|---|---|
| matrix | A table of numbers with rows and columns. | A page of a register. |
| shape | Rows by columns. | How many lines and headings. |
| weight | A number that says how much an input counts. | How many marks each question is worth. |
| weighted sum | Multiply each input by its weight and add the results. | Adding up the marks of every question. |
| intercept | The starting amount before any input is added. | A fixed fee. |
| slope | How much the answer changes when one input rises by one unit. | Extra rent for each extra square metre. |

## Learn the idea

A matrix is a rectangular table of numbers, and its shape is rows by columns. In NumPy a 2-D array holds one home on each row: [[40, 2], [60, 3]] has two homes with two measurements each. A weighted sum multiplies each input by its weight and adds the results. np.dot does this for every row at once. In the invented rule rent = 100000 + 3000 * area + 20000 * rooms, 100000 is the intercept and 3000 and 20000 are weights. The slope for area is the change in rent for one extra square metre, with rooms held fixed. These numbers are supplied for teaching. A model later learns weights from examples.

## Start on paper

Draw a table with two rows and the columns area and rooms. For [40, 2] calculate 3000 * 40 + 20000 * 2 = 160000, then add 100000 to get 260000. Raise the area by 1 with rooms fixed: the answer rises by 3000. Label the columns before you code.

## Worked example

```python
import numpy as np
homes = np.array([[40, 2], [60, 3]])
weights = np.array([3000, 20000])
intercept = 100000
print(homes.shape)
print(homes[0, 1])
predictions = intercept + np.dot(homes, weights)
print(predictions)
```

Run it, then compare: Line one: (2, 2), the shape of two rows and two columns. Line two: 2, the rooms of home 0. Line three: 260000 and 340000, the rents predicted for the two homes.

## Your turn

Add the home [50, 2] as a third row. Predict its result on paper before you run. State the new shape and what each weight means. Explain why these numbers say nothing about real rents in Kampala. Save F04.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation.

## Tutor pacing

10 minutes recall; 20 minutes paper example; 20 minutes run the code slowly together; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120. Visit all five learners and ask what each symbol and unit means before asking them to change it.

Reference: Shape (3, 2). The third prediction is 290000. 3000 is shillings per square metre and 20000 is shillings per room, each holding the other input fixed. The rule is invented.

Repair: If a learner writes homes * weights, show that it multiplies matching elements and does not add them, then use np.dot. If the column meaning is unclear, label the paper table before coding. Recheck independent predictions before ML13.

Record complete, needs repair or absent. Carry unfinished repair into the next core session. Lab evidence goes in that week's portfolio with no second mark.
