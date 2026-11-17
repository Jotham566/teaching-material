# F02 Lists as vectors and ordered measurements

Week 2, fourth teaching day. Complete ML06 first.

## Learn the idea

A scalar is one number. A vector is an ordered collection of numbers: [40, 2] could describe one home with area 40 square metres and 2 rooms. Order and units matter. A Python list can represent this vector. Square brackets create a list; commas separate items. Indexing retrieves one item: home[0] is the first, because Python starts counting positions at zero. len(home) counts items. A for loop repeats indented instructions for each item. This lab reuses the lists and loops from ML05; it adds the mathematical meaning, not a new library.

## Start on paper

Draw two labelled boxes: area_m2 and rooms. Put 40 and 2 in them. Swap the numbers: would this describe the same home? No. The order gives the numbers their meanings. A vector of three item counts [2, 3, 1] is different from a home vector.

## Worked example

```python
home = [40, 2]
print(len(home))
print(home[0])
print(home[1])
counts = [2, 3, 1]
total_items = 0
for count in counts:
    total_items = total_items + count
print(total_items)
```

Expected output: 2, 40, 2, 6 on separate lines.

## Your turn

Create a home vector for 65 square metres and 3 rooms. Print the area and room count separately. Add a text cell labelling the units. Sum item counts [1, 4, 2] with a loop. Save F02.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation. Use the private submission route in START_HERE.md if a hand-in is requested.

## Tutor pacing and explanations

10 minutes recall; 20 minutes paper example; 20 minutes slowly run the code; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120 minutes. Visit all five learners. Ask what each symbol and unit means before asking them to change it.

Reference: 65, 3, total count 7. Do not add area to rooms: the units are different. Accept either loop variable name if explained.

Repair: IndexError usually means a position beyond the list length. A two-item list only has indexes 0 and 1. Explain why [40, 2] + [10, 1] joins lists rather than adding corresponding measurements.

Record complete / needs repair / absent. Carry unfinished repair into the next core session; defer its optional extension to protect foundation learning. Include this evidence in the existing week’s portfolio, without adding a second mark or increasing the assessment weight.
