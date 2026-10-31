# F03 Variation, proportions and probability

Week 3, fourth teaching day. Complete ML09 first.

**Today's question.** Two groups can have the same mean. How can I tell them apart?

## Words for today

| Word | What it means | Think of it like this |
|---|---|---|
| mean | The total shared out equally. | Sharing a bag of mandazi. |
| deviation | A value minus the mean; it can be negative. | How far a mark is from the class average. |
| standard deviation | A typical size of the deviations, in the original unit. | How spread out the marks are. |
| proportion | A part divided by the whole. | 3 blue counters out of 5. |
| probability | How likely an outcome is under stated conditions. | A fair die gives a 6 about once in six throws. |
| observed fraction | What actually happened in a limited number of tries. | Ten throws of a die. |

## Learn the idea

The mean is a total divided by a count. Two groups can have the same mean and different spread. A deviation is a value minus the mean. NumPy finds the mean and the standard deviation of an array: values.mean() and values.std(). Here the numbers describe the whole small group. A proportion is a part divided by a whole, and times 100 it becomes a percentage. A probability describes a chance under stated conditions. An observed fraction estimates it and does not promise the next outcome.

## Start on paper

Put four cards on the table: 2, 2, 6, 6. The mean is 4. The deviations are -2, -2, 2, 2. The standard deviation is 2. Now four cards 4, 4, 4, 4: the same mean, no spread. For a fair six-sided die two of six faces are above 4, so the probability is 2/6. Ten real throws need not give exactly that fraction.

## Worked example

```python
import numpy as np
values = np.array([2, 2, 6, 6])
mean = values.mean()
deviations = values - mean
spread = values.std()
steady = np.array([4, 4, 4, 4])
print(mean, deviations, spread)
print(steady.mean(), steady.std())
print(2 / 6, 2 / 6 * 100)
```

Run it, then compare: Line one: mean 4.0, deviations minus 2, minus 2, 2 and 2, spread 2.0. Line two, the steady group: mean 4.0, spread 0.0. Line three: 0.3333 and 33.33, a chance of 1 in 3, or 33.3 percent.

## Your turn

Repeat for [1, 1, 5, 5]. Explain the mean and spread in words. A bag has 3 blue and 2 red counters. State the chance of blue and its percentage, assuming each counter is equally likely. Save F03.ipynb.

Run all cells from the top, save, close and reopen. Show the instructor your output and explanation.

## Tutor pacing

10 minutes recall; 20 minutes paper example; 20 minutes run the code slowly together; 10 minutes break; 30 minutes learner variation; 20 minutes individual explanation and repair; 10 minutes save and exit check. Total 120. Visit all five learners and ask what each symbol and unit means before asking them to change it.

Reference: Mean 3.0, standard deviation 2.0, probability of blue 3/5 = 0.6 = 60%. NumPy's std divides by the count, which suits a group described in full.

Repair: If the deviations cancel to zero, the learner added the signed deviations without squaring or using std. If a percentage is above 100, the whole was divided by the part.

Record complete, needs repair or absent. Carry unfinished repair into the next core session. Lab evidence goes in that week's portfolio with no second mark.
