# DA13 Instructor guide: NumPy: the numbers underneath pandas

Private. Keep this file out of the student folder.

**Objective.** By the end: you can turn a column into a NumPy array, calculate its mean, median, spread and percentiles, and find unusually large values.

**Question of the day.** How spread out are the daily customer counts, and which sales are unusually large?

Prerequisite: DA12 Checkpoint one: load, summarise, chart and explain.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

Where it overruns: np.percentile with a list of two values returns an array. Print it before using it.

## Block A. Arrays, summaries and percentiles

Each shop counted its customers every day for 60 days: 180 counts in all. .to_numpy() turns a column into an array. np.mean and np.median give the usual summaries and np.percentile gives the value below which a share of the counts fall.

Ask for the prediction first: Predict whether the mean or the median of the daily counts is bigger.

```python
import numpy as np
import pandas as pd
daily = pd.read_csv("sunrise_daily_summary.csv")
customers = daily["customers_counted"].to_numpy()
print(customers.shape)
print(round(np.mean(customers), 1), np.median(customers))
print(np.percentile(customers, [25, 75]))
print(customers.max() - customers.min())
print(np.mean(customers) == daily["customers_counted"].mean())
```

Correct result: The array has shape (180,). The mean is 143.0 and the median 131.5, so the mean is bigger. The 25th and 75th percentiles are 86.75 and 203.75: a quarter of the days had fewer than 87 customers and a quarter had more than 204. The range is 332. The last line prints True, because pandas and NumPy give the same mean.

Investigate, with answers:

- Why are the mean and the median different here? Answer: Three shops of very different sizes are in the same column. The busy shop pulls the mean up.
- What do the two percentiles tell the owner? Answer: Half of all shop-days fall between 87 and 204 customers. That is the usual range of a day.

Modify: Add 50 to every count at once and print the new mean. Answer: 193.0.

```python
busier = customers + 50
```

## Block B. Spread and outliers

The standard deviation says how far values usually sit from their mean. A common rule marks a value as an outlier when it is more than 1.5 times the gap between the quartiles above the upper quartile.

Ask for the prediction first: Predict how many of the 1513 sales are unusually large by that rule.

```python
sunrise = pd.read_csv("sunrise_sales.csv")
values = (sunrise["units"] * sunrise["unit_price_ugx"]).to_numpy()
q1, q3 = np.percentile(values, [25, 75])
fence = q3 + 1.5 * (q3 - q1)
big = values[values > fence]
print(q1, q3, fence)
print(len(big), big.max())
print(round(np.std(customers), 1))
```

Correct result: The quartiles are 1200 and 4500, so the fence is 9450. 137 of the 1513 sales are above it, and the largest is 108000. The standard deviation of the daily customer counts is 73.7. A few large sales sit far out. They are real sales, so we report them and do not delete them.

Investigate, with answers:

- Should we delete the 137 outliers? Answer: No. They are real sales, mostly bulk purchases. We report them and say that they pull the mean up.
- What does a standard deviation of 73.7 customers tell us? Answer: Daily counts typically sit about 74 customers from the mean of 143.

Modify: Count the sales with a value above 20000. Answer: A small number that stays unusual.

```python
n_huge = int((values > 20000).sum())
```

## Make: reference

```python
import numpy as np
import pandas as pd
daily = pd.read_csv("sunrise_daily_summary.csv")
revenue = daily["revenue_ugx"].to_numpy()
np_route = [np.mean(revenue), np.median(revenue)] + list(np.percentile(revenue, [25, 75]))
pd_route = [daily["revenue_ugx"].mean(), daily["revenue_ugx"].median(), daily["revenue_ugx"].quantile(0.25), daily["revenue_ugx"].quantile(0.75)]
assert np.allclose(np_route, pd_route)
print(np_route)
# Mean 35421.67, median 30350, quartiles 18400 and 44125.
```

Evidence to collect: DA13.ipynb with the four numbers from both routes and a passing allclose check.

## Misconceptions to listen for

- An outlier is a mistake and should be deleted.
- NumPy and pandas give different answers.
- The mean and median should be equal.

## Questions to ask, with expected answers

- Why do we not delete outliers automatically? Expected: They may be real. Deleting them changes the story without telling the reader.
- What does np.percentile(x, 75) return? Expected: The value that 75 percent of the numbers fall below.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
