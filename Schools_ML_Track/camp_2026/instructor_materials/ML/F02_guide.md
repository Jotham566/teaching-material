# F02 Lists, vectors and NumPy arrays

Week 2, fourth teaching day. Complete ML06 first.

**Today's question.** Why do the numbers in a list need a fixed order and a unit?

## Words for today

| Word | What it means | Think of it like this |
|---|---|---|
| scalar | A single number. | One mark. |
| vector | An ordered list of numbers whose positions have meanings. | A home described by area, then rooms. |
| NumPy array | A list of numbers that can be calculated with all at once. | A whole row of marks marked together. |
| shape | The size of an array, such as (2,) for two numbers. | Counting the boxes in a row. |
| element-wise | Doing the same calculation to every number. | Adding the same bonus to every pupil's mark. |
| unit | What a number measures, such as square metres. | Shillings, kilograms or metres. |

## Learn the idea

A scalar is one number. A vector is an ordered group of numbers, and the order gives each number its meaning: [40, 2] could be a home with an area of 40 square metres and 2 rooms. A plain Python list can hold a vector, but adding two lists joins them. NumPy arrays calculate element by element. np.array makes an array and its shape tells how many numbers it holds.

## Start on paper

Draw two labelled boxes: area_m2 and rooms. Put 40 and 2 in them. Swap the numbers. Is it still the same home? No, because the order gives the numbers their meanings. Then write what you expect from [40, 2] + [10, 1] and from adding the two as arrays.

## Worked example

```python
import numpy as np
home = [40, 2]
print(len(home))
joined = home + [10, 1]
print(joined)
home_array = np.array([40, 2])
print(home_array.shape)
added = home_array + np.array([10, 1])
doubled = home_array * 2
print(added)
print(doubled)
```

Run it, then compare: 2, then [40, 2, 10, 1] (the lists are joined), then (2,), then [50  3] and [80  4] (calculated one by one).

## Your turn

Make a NumPy array for a home of 65 square metres and 3 rooms. Print its shape. Add a text cell that labels the units of each position. Add the item counts [1, 4, 2] with a loop and then with .sum(). Save F02.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation.

## Tutor pacing

10 minutes recall; 20 minutes paper example; 20 minutes run the code slowly together; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120. Visit all five learners and ask what each symbol and unit means before asking them to change it.

Reference: Shape (2,); a total of 7 both ways. Do not add area to rooms: the units differ. Accept any loop variable name if the learner can explain it.

Repair: An IndexError means a position outside the array. [40, 2] has positions 0 and 1 only. If a learner expects list addition to add numbers, rerun the joined line and compare it with the array line.

Record complete, needs repair or absent. Carry unfinished repair into the next core session. Lab evidence goes in that week's portfolio with no second mark.
