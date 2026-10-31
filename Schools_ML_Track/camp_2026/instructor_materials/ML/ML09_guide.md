# ML09 Instructor guide: Mean, median, range and proportions

Private. Keep this file out of the student folder.

**Objective.** By the end: you can calculate the mean, median, range and a proportion, and say which one an extreme value moves most.

**Question of the day.** What is a typical number of units in a sale, and how spread out are the sales?

Prerequisite: ML08 Select, filter and calculate new columns.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. Typical value and spread

Look at how many units each sale has. Run the cell and read the four numbers.

Ask for the prediction first: Predict whether the mean or the median of the units column is larger.

```python
import numpy as np
import pandas as pd
shop = pd.read_csv("camp_shop.csv")
units = shop["units"]
mean_units = units.mean()
median_units = np.median(units)
spread = units.max() - units.min()
p75 = np.percentile(units, 75)
print(mean_units, median_units, spread, p75)
```

Correct result: The cell prints about 4.62, 4.5, 7 and 7.0. The mean is the total of 277 divided by 60 sales. The median 4.5 sits between the 30th and 31st values in order. The range is 8 minus 1. The 75th percentile 7 means three quarters of the sales have 7 units or fewer. NumPy is the library behind pandas for numbers, and np is its short name.

Investigate, with answers:

- Why is the median 4.5 and not a whole number? Answer: With 60 values the middle falls between two of them, so it is their average.
- What does the 75th percentile tell a shopkeeper? Answer: Three quarters of the sales had 7 units or fewer. Only 10 of the 60 sales had 8, the most any sale had, so stock for 7 or 8 units at a time.

Modify: Find the 25th percentile of units. Answer: 2.0.

```python
p25 = np.percentile(units, 25)
```

## Block B. One extreme value and a proportion

Add one very large value to a small list and see what moves. Then count a proportion.

Ask for the prediction first: Predict which moves more when 100 joins the list: the mean or the median.

```python
small = pd.Series([10, 12, 14, 16])
bigger = pd.Series([10, 12, 14, 16, 100])
print(small.mean(), small.median(), bigger.mean(), bigger.median())
share_big = (units >= 5).sum() / len(units)
print(share_big, share_big * 100)
```

Correct result: The cell prints 13.0, 13.0, 30.4 and 14.0, then 0.5 and 50.0. The outlier 100 pulls the mean from 13 to 30.4 and moves the median only to 14. Half of all sales have 5 units or more: 30 out of 60 is the proportion 0.5, which is 50%.

Investigate, with answers:

- Which summary should you quote when one huge sale sits in the data? Answer: The median, because it hardly moves. Also report the outlier.
- Why must you name the whole when you give a proportion? Answer: 30 out of 60 and 30 out of 300 are very different. The denominator tells what the share is a share of.

Modify: Replace 100 with 1000 in bigger and print the mean and the median. Answer: The mean becomes 210.4 and the median stays 14.0.

```python
bigger = pd.Series([10, 12, 14, 16, 1000])
```

## Make: reference

```python
rate_a = 12 / 20 * 100
rate_b = 15 / 50 * 100
print(rate_a, rate_b)
# 60.0 and 30.0. 15 is the larger count but out of 50, so its rate is lower.
```

Evidence to collect: ML09.ipynb with mean, median and range for [10, 12, 14, 16] before and after adding 100, and the two rates.

## Misconceptions to listen for

- The median and mean are always the same.
- A bigger count means a bigger rate.
- Range tells me what is typical.

## Questions to ask, with expected answers

- When is the mean a poor summary? Expected: When outliers pull it away from where most values sit.
- What is the percentage form of 0.5? Expected: 50%.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
