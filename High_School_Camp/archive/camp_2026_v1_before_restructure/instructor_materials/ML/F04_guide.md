# F04 Matrices, weighted sums and a prediction rule

Week 4, fourth teaching day. Complete ML12 first.

## Learn the idea

A matrix is a rectangular table of numbers. Its shape is rows by columns. For two homes measured by area and room count, a 2 by 2 matrix can be represented by [[40, 2], [60, 3]]. Each inner list is one row. homes[0][1] selects the first home then its room count. A weighted sum multiplies each input by its matching weight and adds the products; this is a dot product for equal-length vectors. In the invented rule rent = 100000 + 3000 * area + 20000 * rooms, 100000 is the intercept (starting amount) and the other numbers are coefficients (weights). They are supplied teaching values, not learned market prices. A model later learns weights from training examples. A line y = b + m*x has intercept b and slope m: slope is the change in y for one extra unit of x. This is rate-of-change intuition, not a calculus qualification.

## Start on paper

Draw a two-row table with columns area and rooms. For [40, 2], calculate 3000*40 + 20000*2 = 160000; add 100000 to get 260000. Increase area by 1 while keeping rooms fixed: the invented output rises by 3000. Never swap column order without also changing its meaning and weights.

## Worked example

```python
homes = [[40, 2], [60, 3]]
weights = [3000, 20000]
intercept = 100000
print(len(homes), len(homes[0]))
print(homes[0][1])
for home in homes:
    weighted_sum = home[0] * weights[0] + home[1] * weights[1]
    prediction = intercept + weighted_sum
    print(prediction)
```

Expected output: 2 2 on the first line, then 2, 260000, 340000 on separate lines.

## Your turn

Add [50, 2] as a third home. Predict its result on paper before running the code. State the matrix shape and what each coefficient means. Explain why these results do not establish real Kampala rent prices. Save F04.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation. Use the private submission route in START_HERE.md if a hand-in is requested.

## Tutor pacing and explanations

10 minutes recall; 20 minutes paper example; 20 minutes slowly run the code; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120 minutes. Visit all five learners. Ask what each symbol and unit means before asking them to change it.

Reference: Shape 3 rows by 2 columns; third prediction 290000. Area coefficient is UGX per square metre, rooms coefficient is UGX per room, holding the other input fixed. The rule is invented, not validated observations.

Repair: If learners try home * weights, revisit corresponding elements: Python lists do not implement vector multiplication. If column meaning is unclear, label the paper table before coding. Recheck independent predictions before ML13.

Record complete / needs repair / absent. Carry unfinished repair into the next core session; defer its optional extension to protect foundation learning. Include this evidence in the existing week’s portfolio, without adding a second mark or increasing the assessment weight.
