# F03 Variation, proportions and probability

Week 3, fourth teaching day. Complete ML09 first.

## Learn the idea

A mean is a total divided by a count. Two lists can have the same mean but different spread. A deviation is a value minus the mean; it can be negative. Squaring means multiplying a number by itself. Population variance is the mean of squared deviations for the complete toy group; standard deviation is its square root and has the original units. We use ** 0.5 to take a square root. This is not an estimate of all students in Uganda. A proportion is a part divided by a whole; multiply by 100 for a percentage. Probability describes the chance of an outcome under specified conditions. An observed fraction estimates a probability; it does not guarantee the next outcome.

## Start on paper

Put four cards labelled 2, 2, 6, 6 on a table. The mean is 4. Deviations are -2, -2, 2, 2; squares are all 4; variance is 4 and standard deviation is 2. Compare with 4, 4, 4, 4: same mean, zero spread. For a fair six-sided die, two of six faces exceed 4: probability 2/6. Ten real throws need not give exactly that fraction.

## Worked example

```python
values = [2, 2, 6, 6]
mean = sum(values) / len(values)
squared_total = 0
for value in values:
    deviation = value - mean
    squared_total = squared_total + deviation * deviation
variance = squared_total / len(values)
print(mean)
print(variance)
print(variance ** 0.5)
print(2 / 6)
print((2 / 6) * 100)
```

Expected output: 4.0, 4.0, 2.0, approximately 0.3333 and 33.3333 on separate lines.

## Your turn

Repeat for [1, 1, 5, 5]. Explain the mean and spread in words. A bag has 3 blue and 2 red counters: state the chance of blue on one random draw and its percentage, assuming each counter is equally likely. Save F03.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation. Use the private submission route in START_HERE.md if a hand-in is requested.

## Tutor pacing and explanations

10 minutes recall; 20 minutes paper example; 20 minutes slowly run the code; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120 minutes. Visit all five learners. Ask what each symbol and unit means before asking them to change it.

Reference: Mean 3, population variance 4, standard deviation 2; probability blue 3/5=0.6=60%. No sample variance denominator is needed because we describe the whole five-counter bag or four-value group.

Repair: If squared deviations cancel to zero, the learner added signed deviations without squaring. If a percentage exceeds 100 here, check that the part is divided by the whole rather than the other way round.

Record complete / needs repair / absent. Carry unfinished repair into the next core session; defer its optional extension to protect foundation learning. Include this evidence in the existing week’s portfolio, without adding a second mark or increasing the assessment weight.
