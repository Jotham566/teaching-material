# DA14 Instructor guide: Exploring distributions with seaborn

Private. Keep this file out of the student folder.

**Objective.** By the end: you can draw a histogram and a box plot with seaborn and describe the shape, the middle and the outliers of a column.

**Question of the day.** What does a typical sale look like, and does it differ between the three shops?

Prerequisite: DA13 NumPy: the numbers underneath pandas.

## The 180 minutes

| Minutes | Activity |
|---|---|
| 10 | Recall: retrieve yesterday, three questions on paper |
| 50 | Block A: predict, run, investigate, modify |
| 15 | Break away from screens |
| 50 | Block B: predict, run, investigate, modify |
| 40 | Make: the independent task and the project journal |
| 15 | Exit ticket, save, and an individual check with each learner |

## Block A. A histogram of sale values

sns.histplot draws a histogram from a DataFrame. Name the DataFrame in data= and the column in x=. A map turns branch ids into names.

Ask for the prediction first: Predict whether the histogram is balanced or skewed to the right.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sunrise = pd.read_csv("sunrise_sales.csv")
sunrise["line_value"] = sunrise["units"] * sunrise["unit_price_ugx"]
sunrise["branch"] = sunrise["branch_id"].map({1: "Central Market", 2: "Campus Gate", 3: "Roadside"})
sns.histplot(data=sunrise, x="line_value", bins=30)
plt.xlabel("Value of one sale (UGX)")
plt.show()
print(round(sunrise["line_value"].skew(), 1))
```

Correct result: The histogram is bunched at the low end with a long tail to the right. The skew is 7.3. A positive skew above 1 means a long right tail. Most sales are small and a few are large.

Investigate, with answers:

- What does the long right tail mean for the mean and the median? Answer: The tail pulls the mean above the median. The median is the better description of a typical sale.
- What does exploratory analysis do that a single total does not? Answer: It shows the shape of the data, so we see the bulk purchases that one total hides.

Modify: Draw the histogram again with bins=60 and say what changes. Answer: The bars get narrower and the long tail shows more detail.

```python
sns.histplot(data=sunrise, x="line_value", bins=60)
plt.close("all")
```

## Block B. A box plot for each shop

sns.boxplot draws one box for each group. The line inside the box is the median. The box runs from the lower quartile to the upper quartile. Dots beyond the whiskers are outliers.

Ask for the prediction first: Predict which shop has the highest median sale.

```python
sns.boxplot(data=sunrise, x="branch", y="line_value")
plt.ylabel("Value of one sale (UGX)")
plt.show()
medians = sunrise.groupby("branch")["line_value"].median()
print(medians)
```

Correct result: The medians are 2500 at Central Market, 2000 at Campus Gate and 2500 at Roadside. The boxes look alike and every shop has dots well above its whiskers: bulk sales happen in all three. The shops differ more in how many sales they make than in how big a typical sale is.

Investigate, with answers:

- Do the shops differ much in typical sale value? Answer: Not much. Two medians are 2500 and one is 2000.
- What do the dots above each box show? Answer: Unusually large sales. They exist at all three shops.

Modify: Use the box plot to compare the units column across shops. Print the median units for each shop. Answer: A similar median at each shop.

```python
unit_medians = sunrise.groupby("branch")["units"].median()
```

## Make: reference

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
daily = pd.read_csv("sunrise_daily_summary.csv")
sns.histplot(data=daily, x="customers_counted", bins=20)
plt.show()
sns.boxplot(data=daily, x="branch", y="customers_counted")
plt.show()
med = daily.groupby("branch")["customers_counted"].median()
print(med)
# Central Market 225, Campus Gate 136, Roadside 87. Central Market has more than twice the customers of Roadside on a typical day.
```

Evidence to collect: DA14.ipynb with a histogram, a box plot, three medians and a finding.

## Misconceptions to listen for

- A box plot shows every value.
- The line in the box is the mean.
- Outlier dots mean the data is wrong.

## Questions to ask, with expected answers

- What does the line in a box plot show? Expected: The median.
- How do you see a skewed distribution in a histogram? Expected: The bars bunch at one end and trail off in a long tail at the other.

## Evidence and feedback

Record complete, needs repair or absent for each of the five learners, with one concrete repair action. Visit every learner, not only volunteers. Keep this guide private. Numeric results come from reference_values.json; explanations and live demonstrations need your judgement and are not auto-graded.
