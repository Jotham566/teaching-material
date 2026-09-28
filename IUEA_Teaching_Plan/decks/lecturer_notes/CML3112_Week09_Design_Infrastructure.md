# CML3112 Week09 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Classification and the cost of mistakes

PURPOSE
Classification and the cost of mistakes

CONNECT
Previous slide: the preceding week.

EXPLAIN
Civil Engineering and Architecture

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Today’s learning.

REFERENCES


## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Previous slide: Classification and the cost of mistakes.

EXPLAIN
Distinguish an actual label from a predicted label.

Count prediction outcomes and explain their costs.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Three independently built classifiers, ROC/AUC and full threshold curves are extension after the basic matrix is secure.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Connection to the previous lesson.

REFERENCES


## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Previous slide: Today’s learning.

EXPLAIN
Week 8 predicted a number. This week predicts a category and counts the different kinds of correct and incorrect result.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Why this week’s tools are needed.

REFERENCES


## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Previous slide: Connection to the previous lesson.

EXPLAIN
A warning system predicts a category. We compare each prediction with its recorded answer, then count false alarms and missed warnings using an explicit cost rule.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The positive class.

REFERENCES


## Slide 5 — The positive class

PURPOSE
The positive class

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
In this example, 1 means a warning is needed.

0 means a warning is not needed.

Actual is the reference label. Predicted is the model’s label.

A false negative misses a real warning.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Class and positive label / TP and TN.

REFERENCES


## Slide 6 — Class and positive label / TP and TN

PURPOSE
Class and positive label / TP and TN

CONNECT
Previous slide: The positive class.

EXPLAIN
Class and positive label: A class is a category. Here 1 means warning and 0 means no warning. Positive means the named class, not good news.

TP and TN: True positive is a correctly flagged warning. True negative is a correctly unflagged non-warning.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
FP and FN.

REFERENCES


## Slide 7 — FP and FN

PURPOSE
FP and FN

CONNECT
Previous slide: Class and positive label / TP and TN.

EXPLAIN
FP and FN: False positive is a false alarm. False negative is a missed warning.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Actual and predicted describe different things.

REFERENCES


## Slide 8 — Actual and predicted describe different things

PURPOSE
Actual and predicted describe different things

CONNECT
Previous slide: FP and FN.

EXPLAIN
Actual is the recorded reference answer.

Predicted is the answer produced by our model.

A correct prediction matches the reference. Class 1 means warning in this example.

LECTURER CUE
Place four paper observations in a table of actual label and predicted label. Classify each before showing the four-cell matrix. State which axis is actual and which is predicted.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Every paired result belongs in one cell.

REFERENCES


## Slide 9 — Every paired result belongs in one cell

PURPOSE
Every paired result belongs in one cell

CONNECT
Previous slide: Actual and predicted describe different things.

EXPLAIN
Read actual first, then predicted. Explain the missed warning.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
The four kinds of result.

REFERENCES


## Slide 10 — The four kinds of result

PURPOSE
The four kinds of result

CONNECT
Previous slide: Every paired result belongs in one cell.

EXPLAIN
Actual / Predicted | Warning 1 | No warning 0

Warning 1 | TP = 1 | FN = 1

No warning 0 | FP = 1 | TN = 1

Rows are actual and columns are predicted.

LECTURER CUE
Rows are actual and columns are predicted. Read each paired observation into exactly one cell. Precision = 1/2. Recall = 1/2. Cost = 5 × FN + FP = 6 under this invented cost rule.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Precision / Recall.

REFERENCES


## Slide 11 — Precision / Recall

PURPOSE
Precision / Recall

CONNECT
Previous slide: The four kinds of result.

EXPLAIN
Precision: Of all predicted warnings, the fraction that were actual warnings: TP / (TP + FP).

Recall: Of all actual warnings, the fraction detected: TP / (TP + FN).

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Precision and recall.

REFERENCES


## Slide 12 — Precision and recall

PURPOSE
Precision and recall

CONNECT
Previous slide: Precision / Recall.

EXPLAIN
Precision asks: of the warnings raised, how many were correct?

Recall asks: of the real warnings, how many did we detect?

A zero denominator needs an explicit rule.

Use the rule in your task brief when implementing the function.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Probability and a decision threshold.

REFERENCES


## Slide 13 — Probability and a decision threshold

PURPOSE
Probability and a decision threshold

CONNECT
Previous slide: Precision and recall.

EXPLAIN
Probability: A probability is between 0 and 1. Multiply by 100 for percent: 0.7 is 70%. A model’s probability is an estimate that needs checking.

Threshold: A threshold turns a score into a decision. For a rule score >= 0.5, a score of 0.7 gives class 1. Use validation data to choose the threshold.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Apply one stated decision threshold.

REFERENCES


## Slide 14 — Apply one stated decision threshold

PURPOSE
Apply one stated decision threshold

CONNECT
Previous slide: Probability and a decision threshold.

EXPLAIN
Estimated positive probability | At least 0.5? | Decision

0.20 | No | Class 0

0.50 | Yes | Class 1

0.80 | Yes | Class 1

0.5 means 50%. This rule includes equality. A probability is an estimate, not a promise that one case is correct.

Read the rows in order. 0.5 means 50%. This rule includes equality. A probability is an estimate, not a promise that one case is correct.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A category decision can use a probability.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 15 — A category decision can use a probability

PURPOSE
A category decision can use a probability

CONNECT
Previous slide: Apply one stated decision threshold.

EXPLAIN
A classifier may estimate the probability of class 1.

A threshold converts that estimate into warning or no warning.

Logistic regression is a classification model. Its probability estimates still need evaluation.

LECTURER CUE
Only after the count exercise, show a classifier fit/predict demonstration. Logistic regression predicts a category despite its name. Probability estimates need not be well calibrated.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Threshold and cost.

REFERENCES


## Slide 16 — Threshold and cost

PURPOSE
Threshold and cost

CONNECT
Previous slide: A category decision can use a probability.

EXPLAIN
Threshold and cost: A threshold converts a score to a decision. A cost rule states how much each type of mistake matters. Lower thresholds usually increase recall; precision need not decrease at every step.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
State the cost rule before calculating.

REFERENCES


## Slide 17 — State the cost rule before calculating

PURPOSE
State the cost rule before calculating

CONNECT
Previous slide: Threshold and cost.

EXPLAIN
A cost rule assigns a penalty to each kind of mistake. In this teaching example, a missed warning costs 5 units and a false alarm costs 1 unit.

Total cost = 5 × FN + FP. One missed warning and one false alarm therefore cost 6 units.

These are invented teaching penalties. Use the published assignment cost rule and explain whose consequences it represents.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting syntax in the example.

REFERENCES


## Slide 18 — Counting syntax in the example

PURPOSE
Counting syntax in the example

CONNECT
Previous slide: State the cost rule before calculating.

EXPLAIN
Code | Equivalent idea

tp = tn = fp = fn = 0 | Set each of four counts to zero

tp += 1 | tp = tp + 1

zip(actual, predicted) | Pair items in the same positions

elif condition: | Try this branch if earlier ones failed

Our paired lists must have matching lengths. zip alone stops at the shorter list.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example.

REFERENCES


## Slide 19 — Classification outcomes in Python

PURPOSE
Classification outcomes in Python

CONNECT
Previous slide: Counting syntax in the example.

EXPLAIN
Read the code in this order:
actual = [1, 1, 0, 0]
predicted = [1, 0, 1, 0]
for truth, guess in zip(actual, predicted):
    print(truth, guess)
# Count the four categories on paper before calculating.
tp, fn, fp, tn = 1, 1, 1, 1
print(tp / (tp + fp))
print(tp / (tp + fn))
print(5 * fn + fp)

for takes the next item. The indented block repeats.

zip pairs items at matching positions in these equal-length lists.

print displays a value below the cell.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Place four paper observations in a table of actual label and predicted label. Classify each before showing the four-cell matrix. State which axis is actual and which is predicted. Use counts before fractions. The denominator of precision is predicted positives; the denominator of recall is actual positives. Explain what happens if either denominator is zero. Only after the count exercise, show a classifier fit/predict demonstration. Logistic regression predicts a category despite its name. Probability estimates need not be well calibrated.

Complete practice code:
actual = [1, 1, 0, 0]
predicted = [1, 0, 1, 0]
for truth, guess in zip(actual, predicted):
    print(truth, guess)
# Count the four categories on paper before calculating.
tp, fn, fp, tn = 1, 1, 1, 1
print(tp / (tp + fp))
print(tp / (tp + fn))
print(5 * fn + fp)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 20 — Classification outcomes results

PURPOSE
Classification outcomes results

CONNECT
Previous slide: Classification outcomes in Python.

EXPLAIN
Four paired rows, then precision 0.5, recall 0.5 and teaching cost 6.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the four counters.

REFERENCES


## Slide 21 — Trace the four counters

PURPOSE
Trace the four counters

CONNECT
Previous slide: Classification outcomes results.

EXPLAIN
Actual, predicted | Chosen counter | Counts: TP TN FP FN

1, 1 | TP increases | 1 0 0 0

1, 0 | FN increases | 1 0 0 1

0, 1 | FP increases | 1 0 1 1

0, 0 | TN increases | 1 1 1 1

All counts start at zero. Each observation follows exactly one if/elif/else branch.

Read the rows in order. All counts start at zero. Each observation follows exactly one if/elif/else branch.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting arbitrary paired observations.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 22 — Counting arbitrary paired observations

PURPOSE
Counting arbitrary paired observations

CONNECT
Previous slide: Trace the four counters.

EXPLAIN
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

tp = tn = fp = fn = 0 sets all four counters to zero. tp += 1 is shorthand for tp = tp + 1.

LECTURER CUE
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting arbitrary paired observations in Python (1/3).

REFERENCES


## Slide 23 — Counting arbitrary paired observations in Python (1/3)

PURPOSE
Counting arbitrary paired observations in Python (1/3)

CONNECT
Previous slide: Counting arbitrary paired observations.

EXPLAIN
Read the code in this order:
tp = tn = fp = fn = 0

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

Complete practice code:
tp = tn = fp = fn = 0
for truth, guess in zip(actual, predicted):
    if truth == 1 and guess == 1:
        tp += 1
    elif truth == 0 and guess == 0:
        tn += 1
    elif truth == 0 and guess == 1:
        fp += 1
    else:
        fn += 1
print(tp, tn, fp, fn)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting arbitrary paired observations in Python (2/3).

REFERENCES


## Slide 24 — Counting arbitrary paired observations in Python (2/3)

PURPOSE
Counting arbitrary paired observations in Python (2/3)

CONNECT
Previous slide: Counting arbitrary paired observations in Python (1/3).

EXPLAIN
Read the code in this order:
for truth, guess in zip(actual, predicted):
    if truth == 1 and guess == 1:
        tp += 1
    elif truth == 0 and guess == 0:
        tn += 1
    elif truth == 0 and guess == 1:
        fp += 1
    else:
        fn += 1

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

zip pairs items at matching positions in these equal-length lists.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

Complete practice code:
tp = tn = fp = fn = 0
for truth, guess in zip(actual, predicted):
    if truth == 1 and guess == 1:
        tp += 1
    elif truth == 0 and guess == 0:
        tn += 1
    elif truth == 0 and guess == 1:
        fp += 1
    else:
        fn += 1
print(tp, tn, fp, fn)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Counting arbitrary paired observations in Python (3/3).

REFERENCES


## Slide 25 — Counting arbitrary paired observations in Python (3/3)

PURPOSE
Counting arbitrary paired observations in Python (3/3)

CONNECT
Previous slide: Counting arbitrary paired observations in Python (2/3).

EXPLAIN
Read the code in this order:
print(tp, tn, fp, fn)

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

Complete practice code:
tp = tn = fp = fn = 0
for truth, guess in zip(actual, predicted):
    if truth == 1 and guess == 1:
        tp += 1
    elif truth == 0 and guess == 0:
        tn += 1
    elif truth == 0 and guess == 1:
        fp += 1
    else:
        fn += 1
print(tp, tn, fp, fn)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Represent a category with indicators.

REFERENCES


## Slide 26 — Represent a category with indicators

PURPOSE
Represent a category with indicators

CONNECT
Previous slide: Counting arbitrary paired observations in Python (3/3).

EXPLAIN
Category: A category is a label such as steel or timber. Its name does not imply a numerical size or rank.

One-hot indicator: Create a column for each category. Its entry is 1 when the row has that category and 0 otherwise. Learn the allowed categories from training data.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A category can become indicator columns.

REFERENCES


## Slide 27 — A category can become indicator columns

PURPOSE
A category can become indicator columns

CONNECT
Previous slide: Represent a category with indicators.

EXPLAIN
Material | is_steel | is_timber

steel | 1 | 0

timber | 0 | 1

An encoder converts category labels to numeric columns. Fit it on training data. Each indicator is 1 when that category applies, otherwise 0.

LECTURER CUE
An indicator is 1 when its category applies and 0 otherwise. Fit the encoder on training data.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Accuracy can hide missed warnings.

REFERENCES


## Slide 28 — Accuracy can hide missed warnings

PURPOSE
Accuracy can hide missed warnings

CONNECT
Previous slide: A category can become indicator columns.

EXPLAIN
Accuracy = number of correct labels / number of labels. It counts correct warnings and correct non-warnings together.

If 90 of 100 cases need no warning, predicting no warning every time gives 90% accuracy. It detects none of the 10 real warnings: recall is 0.

Always inspect the actual/predicted counts and relevant costs before calling a classifier useful.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 29 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Accuracy can hide missed warnings.

EXPLAIN
Example: Change the second prediction to 1. Count again. Does this improve both recall and the assumed cost?

Answer: TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 30 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
Implement classification_metrics on arbitrary paired binary labels, not only the example.

Use the published zero-denominator convention.

Read the supplied W09 comparison separately.

Teacher-written cost assumptions are not approved operating limits.

LECTURER CUE
Implement classification_metrics on arbitrary paired binary labels, not only the example. Use the published zero-denominator convention. Read the supplied W09 comparison separately. Teacher-written cost assumptions are not approved operating limits. All claimed benefits require real-world evaluation.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 31 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
All claimed benefits require real-world evaluation.

LECTURER CUE
Implement classification_metrics on arbitrary paired binary labels, not only the example. Use the published zero-denominator convention. Read the supplied W09 comparison separately. Teacher-written cost assumptions are not approved operating limits. All claimed benefits require real-world evaluation.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Category predictions and operating thresholds.

REFERENCES


## Slide 32 — Category predictions and operating thresholds

PURPOSE
Category predictions and operating thresholds

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
A majority-only classifier can achieve high accuracy while missing the rare class.

Name the positive class and both confusion-matrix axes.

A model expecting numeric features cannot directly use raw category strings; use numeric indicator columns for categories.

Compare threshold choices on validation data.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Category predictions and operating thresholds continued.

REFERENCES


## Slide 33 — Category predictions and operating thresholds continued

PURPOSE
Category predictions and operating thresholds continued

CONNECT
Previous slide: Category predictions and operating thresholds.

EXPLAIN
Reducing the threshold adds flagged cases and cannot reduce recall on fixed scored observations, but precision can move either way.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task.

REFERENCES


## Slide 34 — Your issued task

PURPOSE
Your issued task

CONNECT
Previous slide: Category predictions and operating thresholds continued.

EXPLAIN
Use classification_case.csv.

Positive means a synthetic warning condition.

Compute the confusion matrix, precision, recall and cost.

Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient.

LECTURER CUE
Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task continued.

REFERENCES


## Slide 35 — Your issued task continued

PURPOSE
Your issued task continued

CONNECT
Previous slide: Your issued task.

EXPLAIN
These costs are teaching assumptions, not approved operating limits.

LECTURER CUE
Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
classification_metrics(actual, predicted).

REFERENCES


## Slide 36 — classification_metrics(actual, predicted)

PURPOSE
classification_metrics(actual, predicted)

CONNECT
Previous slide: Your issued task continued.

EXPLAIN
For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W09/CML3112/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 37 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: classification_metrics(actual, predicted).

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Classification and cost submission.

REFERENCES


## Slide 38 — Classification and cost submission

PURPOSE
Classification and cost submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 03 Nov 2026, 11:00 Kampala

Deadline: 10 Nov 2026, 11:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 9 quiz.

REFERENCES


## Slide 39 — Week 9 quiz

PURPOSE
Week 9 quiz

CONNECT
Previous slide: Classification and cost submission.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W9_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 40 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 9 quiz.

EXPLAIN
You can identify a false negative and explain precision and recall with counts.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 41 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals The Confusion Matrix

Opening up to 04:00, optional preview-selected excerpt

Listening question: Which observations are correctly or incorrectly classified?

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Translate the medical example to warning/no-warning and label the axes.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=Kdsp6soqA7o

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
