# CML3111 Week09 Engineering

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Classification and the cost of mistakes

Classification and the cost of mistakes
CML3111, Week 9, slide 1

Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3111, Week 9, slide 2

Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Distinguish an actual label from a predicted label.

Count prediction outcomes and explain their costs.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3111, Week 9, slide 3

Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Week 8 predicted a number. This week predicts a category and counts the different kinds of correct and incorrect result.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3111, Week 9, slide 4

Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
A warning system predicts a category. We compare each prediction with its recorded answer, then count false alarms and missed warnings using an explicit cost rule.

Continue to
The positive class

## Slide 5 — The positive class

The positive class
CML3111, Week 9, slide 5

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
In this example, 1 means a warning is needed.

0 means a warning is not needed.

Actual is the reference label. Predicted is the model’s label.

A false negative misses a real warning.

Continue to
Class and positive label / TP and TN

## Slide 6 — Class and positive label / TP and TN

Class and positive label / TP and TN
CML3111, Week 9, slide 6

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
Class and positive label: A class is a category. Here 1 means warning and 0 means no warning. Positive means the named class, not good news.
TP and TN: True positive is a correctly flagged warning. True negative is a correctly unflagged non-warning.

Continue to
FP and FN

## Slide 7 — FP and FN

FP and FN
CML3111, Week 9, slide 7

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
FP and FN: False positive is a false alarm. False negative is a missed warning.

Continue to
Actual and predicted describe different things

## Slide 8 — Actual and predicted describe different things

Actual and predicted describe different things
CML3111, Week 9, slide 8

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
Actual is the recorded reference answer.

Predicted is the answer produced by our model.

A correct prediction matches the reference. Class 1 means warning in this example.

Continue to
Every paired result belongs in one cell

## Slide 9 — Every paired result belongs in one cell

Every paired result belongs in one cell
CML3111, Week 9, slide 9

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
Read actual first, then predicted. Explain the missed warning.

Continue to
The four kinds of result

## Slide 10 — The four kinds of result

The four kinds of result
CML3111, Week 9, slide 10

Explanation to give
First name what 1 means. Read the actual label before the prediction. True/false refers to whether the prediction is correct; positive/negative refers to the predicted class.

Worked illustration / lecturer answer
With 1 meaning warning: actual 1, predicted 0 is a false negative, a missed warning. Actual 0, predicted 1 is a false positive, an unnecessary warning.

Misconception to address
Positive does not mean good. A high count of correct normal cases can hide a dangerous number of missed warnings.

On this slide
Actual / Predicted | Warning 1 | No warning 0
Warning 1 | TP = 1 | FN = 1
No warning 0 | FP = 1 | TN = 1
Rows are actual and columns are predicted.

Continue to
Precision / Recall

## Slide 11 — Precision / Recall

Precision / Recall
CML3111, Week 9, slide 11

Explanation to give
Use two different denominators. Precision looks only at issued warnings. Recall looks only at real cases that needed a warning. Say the population in the denominator before calculating.

Worked illustration / lecturer answer
If TP=3, FP=1 and FN=2, precision is 3/(3+1)=0.75 and recall is 3/(3+2)=0.60. One asks whether warnings are reliable; the other asks whether true problems were found.

Misconception to address
The denominators are not interchangeable. Follow the published convention when a denominator is zero and explain why that case arises.

On this slide
Precision: Of all predicted warnings, the fraction that were actual warnings: TP / (TP + FP).
Recall: Of all actual warnings, the fraction detected: TP / (TP + FN).

Continue to
Precision and recall

## Slide 12 — Precision and recall

Precision and recall
CML3111, Week 9, slide 12

Explanation to give
Use two different denominators. Precision looks only at issued warnings. Recall looks only at real cases that needed a warning. Say the population in the denominator before calculating.

Worked illustration / lecturer answer
If TP=3, FP=1 and FN=2, precision is 3/(3+1)=0.75 and recall is 3/(3+2)=0.60. One asks whether warnings are reliable; the other asks whether true problems were found.

Misconception to address
The denominators are not interchangeable. Follow the published convention when a denominator is zero and explain why that case arises.

On this slide
Precision asks: of the warnings raised, how many were correct?

Recall asks: of the real warnings, how many did we detect?

A zero denominator needs an explicit rule.

Use the rule in your task brief when implementing the function.

Continue to
Probability and a decision threshold

## Slide 13 — Probability and a decision threshold

Probability and a decision threshold
CML3111, Week 9, slide 13

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
Probability: A probability is between 0 and 1. Multiply by 100 for percent: 0.7 is 70%. A model’s probability is an estimate that needs checking.
Threshold: A threshold turns a score into a decision. For a rule score >= 0.5, a score of 0.7 gives class 1. Use validation data to choose the threshold.

Continue to
Apply one stated decision threshold

## Slide 14 — Apply one stated decision threshold

Apply one stated decision threshold
CML3111, Week 9, slide 14

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
Estimated positive probability | At least 0.5? | Decision
0.20 | No | Class 0
0.50 | Yes | Class 1
0.80 | Yes | Class 1
0.5 means 50%. This rule includes equality. A probability is an estimate, not a promise that one case is correct.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
A category decision can use a probability

## Slide 15 — A category decision can use a probability

A category decision can use a probability
CML3111, Week 9, slide 15

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
A classifier may estimate the probability of class 1.

A threshold converts that estimate into warning or no warning.

Logistic regression is a classification model. Its probability estimates still need evaluation.

Continue to
Threshold and cost

## Slide 16 — Threshold and cost

Threshold and cost
CML3111, Week 9, slide 16

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
Threshold and cost: A threshold converts a score to a decision. A cost rule states how much each type of mistake matters. Lower thresholds usually increase recall; precision need not decrease at every step.

Continue to
State the cost rule before calculating

## Slide 17 — State the cost rule before calculating

State the cost rule before calculating
CML3111, Week 9, slide 17

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
A cost rule assigns a penalty to each kind of mistake. In this teaching example, a missed warning costs 5 units and a false alarm costs 1 unit.

Total cost = 5 × FN + FP. One missed warning and one false alarm therefore cost 6 units.

These are invented teaching penalties. Use the published assignment cost rule and explain whose consequences it represents.

Continue to
Counting syntax in the example

## Slide 18 — Counting syntax in the example

Counting syntax in the example
CML3111, Week 9, slide 18

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

On this slide
Code | Equivalent idea
tp = tn = fp = fn = 0 | Set each of four counts to zero
tp += 1 | tp = tp + 1
zip(actual, predicted) | Pair items in the same positions
elif condition: | Try this branch if earlier ones failed
Our paired lists must have matching lengths. zip alone stops at the shorter list.

Continue to
Classification outcomes in Python

## Slide 19 — Classification outcomes in Python

Classification outcomes in Python
CML3111, Week 9, slide 19

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

Read the displayed code line by line
actual = [1, 1, 0, 0]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

predicted = [1, 0, 1, 0]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for truth, guess in zip(actual, predicted):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

print(truth, guess)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

tp, fn, fp, tn = 1, 1, 1, 1
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(tp / (tp + fp))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(tp / (tp + fn))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

print(5 * fn + fp)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Classification outcomes results

## Slide 20 — Classification outcomes results

Classification outcomes results
CML3111, Week 9, slide 20

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

On this slide
Four paired rows, then precision 0.5, recall 0.5 and teaching cost 6.

Continue to
Trace the four counters

## Slide 21 — Trace the four counters

Trace the four counters
CML3111, Week 9, slide 21

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

On this slide
Actual, predicted | Chosen counter | Counts: TP TN FP FN
1, 1 | TP increases | 1 0 0 0
1, 0 | FN increases | 1 0 0 1
0, 1 | FP increases | 1 0 1 1
0, 0 | TN increases | 1 1 1 1
All counts start at zero. Each observation follows exactly one if/elif/else branch.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Counting arbitrary paired observations

## Slide 22 — Counting arbitrary paired observations

Counting arbitrary paired observations
CML3111, Week 9, slide 22

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

On this slide
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

tp = tn = fp = fn = 0 sets all four counters to zero. tp += 1 is shorthand for tp = tp + 1.

Continue to
Counting arbitrary paired observations in Python (1/3)

## Slide 23 — Counting arbitrary paired observations in Python (1/3)

Counting arbitrary paired observations in Python (1/3)
CML3111, Week 9, slide 23

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

Read the displayed code line by line
tp = tn = fp = fn = 0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Counting arbitrary paired observations in Python (2/3)

## Slide 24 — Counting arbitrary paired observations in Python (2/3)

Counting arbitrary paired observations in Python (2/3)
CML3111, Week 9, slide 24

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

Read the displayed code line by line
for truth, guess in zip(actual, predicted):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if truth == 1 and guess == 1:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

tp += 1
Add the right-hand amount to the current stored value, then keep the updated value.

elif truth == 0 and guess == 0:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

tn += 1
Add the right-hand amount to the current stored value, then keep the updated value.

elif truth == 0 and guess == 1:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

fp += 1
Add the right-hand amount to the current stored value, then keep the updated value.

else:
Use this remaining path when the matching earlier condition did not succeed.

fn += 1
Add the right-hand amount to the current stored value, then keep the updated value.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Counting arbitrary paired observations in Python (3/3)

## Slide 25 — Counting arbitrary paired observations in Python (3/3)

Counting arbitrary paired observations in Python (3/3)
CML3111, Week 9, slide 25

Explanation to give
Work through each actual/predicted pair once and increment exactly one counter. Initialising all four counters to zero makes the later counts auditable.

Worked illustration / lecturer answer
A pair (1,0) adds one to FN. A pair (0,1) adds one to FP. After processing n pairs, TP + TN + FP + FN must equal n.

Misconception to address
If separate overlapping conditions increment two counters for one observation, the total exceeds n. Use mutually exclusive cases and verify the total.

Read the displayed code line by line
print(tp, tn, fp, fn)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Represent a category with indicators

## Slide 26 — Represent a category with indicators

Represent a category with indicators
CML3111, Week 9, slide 26

Explanation to give
One-hot encoding gives each category its own indicator column. A row has a 1 in the column matching its category and 0 in the others.

Worked illustration / lecturer answer
For categories A and B, an A row becomes [1,0] and a B row becomes [0,1]. Assigning A=1 and B=2 could accidentally suggest a meaningful numerical distance or order.

Misconception to address
Fit the encoder on training data and define how to handle categories not seen during training. Do not invent an ordinal meaning for names.

On this slide
Category: A category is a label such as steel or timber. Its name does not imply a numerical size or rank.
One-hot indicator: Create a column for each category. Its entry is 1 when the row has that category and 0 otherwise. Learn the allowed categories from training data.

Continue to
A category can become indicator columns

## Slide 27 — A category can become indicator columns

A category can become indicator columns
CML3111, Week 9, slide 27

Explanation to give
One-hot encoding gives each category its own indicator column. A row has a 1 in the column matching its category and 0 in the others.

Worked illustration / lecturer answer
For categories A and B, an A row becomes [1,0] and a B row becomes [0,1]. Assigning A=1 and B=2 could accidentally suggest a meaningful numerical distance or order.

Misconception to address
Fit the encoder on training data and define how to handle categories not seen during training. Do not invent an ordinal meaning for names.

On this slide
Material | is_steel | is_timber
steel | 1 | 0
timber | 0 | 1
An encoder converts category labels to numeric columns. Fit it on training data. Each indicator is 1 when that category applies, otherwise 0.

Continue to
Accuracy can hide missed warnings

## Slide 28 — Accuracy can hide missed warnings

Accuracy can hide missed warnings
CML3111, Week 9, slide 28

Explanation to give
Accuracy counts all correct classifications together. In an imbalanced dataset, correct majority-class answers can dominate the score while the minority class is consistently missed.

Worked illustration / lecturer answer
With 95 normal cases and 5 genuine faults, always predicting normal gives 95% accuracy but detects zero faults. Fault recall is zero.

Misconception to address
A high headline accuracy alone is insufficient for a warning system. Report the confusion counts and the relevant costs.

On this slide
Accuracy = number of correct labels / number of labels. It counts correct warnings and correct non-warnings together.

If 90 of 100 cases need no warning, predicting no warning every time gives 90% accuracy. It detects none of the 10 real warnings: recall is 0.

Always inspect the actual/predicted counts and relevant costs before calling a classifier useful.

Continue to
Revision example and answer

## Slide 29 — Revision example and answer

Revision example and answer
CML3111, Week 9, slide 29

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: Change the second prediction to 1. Count again. Does this improve both recall and the assumed cost?

Answer: TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 30 — Preparing for the assignment

Preparing for the assignment
CML3111, Week 9, slide 30

Explanation to give
Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.

Worked illustration / lecturer answer
MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.

Misconception to address
Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.

On this slide
Implement classification_metrics on arbitrary paired binary labels, not only the example.

Use the published zero-denominator convention.

Read the supplied W09 comparison separately.

Teacher-written cost assumptions are not approved operating limits.

Continue to
Preparing for the assignment continued

## Slide 31 — Preparing for the assignment continued

Preparing for the assignment continued
CML3111, Week 9, slide 31

Explanation to give
The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.

Worked illustration / lecturer answer
Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.

Misconception to address
These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.

On this slide
All claimed benefits require real-world evaluation.

Continue to
Category predictions and operating thresholds

## Slide 32 — Category predictions and operating thresholds

Category predictions and operating thresholds
CML3111, Week 9, slide 32

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
A majority-only classifier can achieve high accuracy while missing the rare class.

Name the positive class and both confusion-matrix axes.

A model expecting numeric features cannot directly use raw category strings; use numeric indicator columns for categories.

Compare threshold choices on validation data.

Continue to
Category predictions and operating thresholds continued

## Slide 33 — Category predictions and operating thresholds continued

Category predictions and operating thresholds continued
CML3111, Week 9, slide 33

Explanation to give
A probability-like score becomes a class decision only after choosing a threshold. The threshold expresses an operating trade-off; an error-cost rule states which mistakes matter more for this task.

Worked illustration / lecturer answer
At threshold >= 0.6, scores 0.59 and 0.60 give 0 and 1. Lowering the threshold usually raises more warnings, potentially reducing misses while increasing false alarms.

Misconception to address
A score of 0.8 is not a guarantee that this particular prediction is right. Evaluate calibration if probabilities will be interpreted literally. Costs must come from the stated scenario.

On this slide
Reducing the threshold adds flagged cases and cannot reduce recall on fixed scored observations, but precision can move either way.

Continue to
Your issued task

## Slide 34 — Your issued task

Your issued task
CML3111, Week 9, slide 34

Explanation to give
The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.

Worked illustration / lecturer answer
Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.

Misconception to address
These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.

On this slide
Use classification_case.csv.

Positive means a synthetic warning condition.

Compute the confusion matrix, precision, recall and cost.

Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient.

Continue to
Your issued task continued

## Slide 35 — Your issued task continued

Your issued task continued
CML3111, Week 9, slide 35

Explanation to give
The warning labels and costs belong to this teaching scenario. Name what positive means before discussing benefit or harm.

Worked illustration / lecturer answer
Compute the confusion counts from aligned actual/predicted labels, then apply the published cost weights. A false alarm and a missed warning can have different costs.

Misconception to address
These illustrative costs are not approved operational thresholds. Claimed benefits need evaluation on relevant real observations before use in engineering decisions.

On this slide
These costs are teaching assumptions, not approved operating limits.

Continue to
classification_metrics(actual, predicted)

## Slide 36 — classification_metrics(actual, predicted)

classification_metrics(actual, predicted)
CML3111, Week 9, slide 36

Explanation to give
Count the four mutually exclusive actual/predicted cases, then calculate the specified fractions and cost from those counts.

Worked illustration / lecturer answer
Verify TP+TN+FP+FN equals the number of paired observations. Read the cost weights and zero-denominator convention from the issued brief.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.

Continue to
Written evidence

## Slide 37 — Written evidence

Written evidence
CML3111, Week 9, slide 37

Explanation to give
Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.

Worked illustration / lecturer answer
A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.

Misconception to address
Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.

On this slide
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

Continue to
Classification and cost submission

## Slide 38 — Classification and cost submission

Classification and cost submission
CML3111, Week 9, slide 38

Explanation to give
This slide hands over CML3111 W09. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-13T11:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 06 Nov 2026, 11:00 Kampala

Deadline: 13 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Week 9 quiz

## Slide 39 — Week 9 quiz

Week 9 quiz
CML3111, Week 9, slide 39

Explanation to give
This is the CML3111 Week 9 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W9_CML3111 when ready and read the logged closing time.

Worked illustration / lecturer answer
Explain the distinction between the expected answering time and availability: five minutes of questions can still be available for 24 hours after activation. Enter the learner’s own Student Registration Number and use the registered Google account.

Misconception to address
Read the exact live cutoff before announcing it. Do not promise a new attempt to somebody who already submitted. Quiz catch-up and assignment uploads are separate forms.

On this slide
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

Check the announced quiz closing time.

Continue to
Revision and submission checklist

## Slide 40 — Revision and submission checklist

Revision and submission checklist
CML3111, Week 9, slide 40

Explanation to give
Move from a numerical prediction to a category decision. Name the positive class before counting correct warnings, false alarms and missed warnings.

Worked illustration / lecturer answer
Actual 1 with predicted 0 is a false negative. If 1 means warning, this is a missed warning, not merely a wrong number.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can identify a false negative and explain precision and recall with counts.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 41 — Optional revision video

Optional revision video
CML3111, Week 9, slide 41

Explanation to give
Give the viewing question before playing the excerpt: Which observations are correctly or incorrectly classified?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals The Confusion Matrix

Opening up to 04:00, optional preview-selected excerpt

Listening question: Which observations are correctly or incorrectly classified?

Reference / existing resource
https://www.youtube.com/watch?v=Kdsp6soqA7o
