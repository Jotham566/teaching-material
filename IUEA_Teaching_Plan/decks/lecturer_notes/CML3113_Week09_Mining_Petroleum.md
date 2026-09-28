# CML3113 Week09 Mining Petroleum

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Classification and the cost of mistakes

PURPOSE
Classification and the cost of mistakes

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Mining and Petroleum Engineering

LECTURER DETAIL
TEACHING PURPOSE
Classification and the cost of mistakes

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Today’s learning.

## Slide 2 — Today’s learning

PURPOSE
Today’s learning

CONNECT
Build on Classification and the cost of mistakes. Explain why this example is needed before running it.

EXPLAIN
Distinguish an actual label from a predicted label.

Count prediction outcomes and explain their costs.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Classification and the cost of mistakes.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Three independently built classifiers, ROC/AUC and full threshold curves are extension after the basic matrix is secure.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Recall and a first attempt. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Connection to the previous lesson.

## Slide 3 — Connection to the previous lesson

PURPOSE
Connection to the previous lesson

CONNECT
Build on Today’s learning. Explain why this example is needed before running it.

EXPLAIN
Week 8 predicted a number. This week predicts a category and counts the different kinds of correct and incorrect result.

LECTURER DETAIL
TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Why this week’s tools are needed.

## Slide 4 — Why this week’s tools are needed

PURPOSE
Why this week’s tools are needed

CONNECT
Build on Connection to the previous lesson. Explain why this example is needed before running it.

EXPLAIN
A warning system predicts a category. We compare each prediction with its recorded answer, then count false alarms and missed warnings using an explicit cost rule.

LECTURER DETAIL
TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A pump team records temperature to investigate operation. Mining students can relate this to a dewatering pump; petroleum students to a transfer pump. These are teaching examples, not operating limits.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
The positive class. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The positive class.

## Slide 5 — The positive class

PURPOSE
The positive class

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
In this example, 1 means a warning is needed.

0 means a warning is not needed.

Actual is the reference label. Predicted is the model’s label.

A false negative misses a real warning.

LECTURER DETAIL
TEACHING PURPOSE
The positive class

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Class and positive label / TP and TN. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Class and positive label / TP and TN.

## Slide 6 — Class and positive label / TP and TN

PURPOSE
Class and positive label / TP and TN

CONNECT
Build on The positive class. Explain why this example is needed before running it.

EXPLAIN
Class and positive label: A class is a category. Here 1 means warning and 0 means no warning. Positive means the named class, not good news.
TP and TN: True positive is a correctly flagged warning. True negative is a correctly unflagged non-warning.

LECTURER DETAIL
TEACHING PURPOSE
Class and positive label / TP and TN

CONNECT
Build on the preceding slide: The positive class.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

POINT TO THE DEFINITION
Class and positive label: A class is a category. Here 1 means warning and 0 means no warning. Positive means the named class, not good news.
TP and TN: True positive is a correctly flagged warning. True negative is a correctly unflagged non-warning.

NEXT
FP and FN. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
FP and FN.

## Slide 7 — FP and FN

PURPOSE
FP and FN

CONNECT
Build on Class and positive label / TP and TN. Explain why this example is needed before running it.

EXPLAIN
FP and FN: False positive is a false alarm. False negative is a missed warning.

LECTURER DETAIL
TEACHING PURPOSE
FP and FN

CONNECT
Build on the preceding slide: Class and positive label / TP and TN.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

POINT TO THE DEFINITION
FP and FN: False positive is a false alarm. False negative is a missed warning.

NEXT
Actual and predicted describe different things. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Actual and predicted describe different things.

## Slide 8 — Actual and predicted describe different things

PURPOSE
Actual and predicted describe different things

CONNECT
Build on FP and FN. Explain why this example is needed before running it.

EXPLAIN
Actual is the recorded reference answer.

Predicted is the answer produced by our model.

A correct prediction matches the reference. Class 1 means warning in this example.

LECTURER DETAIL
TEACHING PURPOSE
Actual and predicted describe different things

CONNECT
Build on the preceding slide: FP and FN.

LECTURER CUE
Place four paper observations in a table of actual label and predicted label. Classify each before showing the four-cell matrix. State which axis is actual and which is predicted.

NEXT
Every paired result belongs in one cell. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Every paired result belongs in one cell.

## Slide 9 — Every paired result belongs in one cell

PURPOSE
Every paired result belongs in one cell

CONNECT
Build on Actual and predicted describe different things. Explain why this example is needed before running it.

EXPLAIN
Read actual first, then predicted. Explain the missed warning.

LECTURER DETAIL
TEACHING PURPOSE
Every paired result belongs in one cell

CONNECT
Build on the preceding slide: Actual and predicted describe different things.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The four kinds of result. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
The four kinds of result.

## Slide 10 — The four kinds of result

PURPOSE
The four kinds of result

CONNECT
Build on Every paired result belongs in one cell. Explain why this example is needed before running it.

EXPLAIN
Rows are actual and columns are predicted.

LECTURER DETAIL
TEACHING PURPOSE
The four kinds of result

CONNECT
Build on the preceding slide: Every paired result belongs in one cell.

LECTURER CUE
Rows are actual and columns are predicted. Read each paired observation into exactly one cell. Precision = 1/2. Recall = 1/2. Cost = 5 × FN + FP = 6 under this invented cost rule.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Precision / Recall. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Precision / Recall.

## Slide 11 — Precision / Recall

PURPOSE
Precision / Recall

CONNECT
Build on The four kinds of result. Explain why this example is needed before running it.

EXPLAIN
Precision: Of all predicted warnings, the fraction that were actual warnings: TP / (TP + FP).
Recall: Of all actual warnings, the fraction detected: TP / (TP + FN).

LECTURER DETAIL
TEACHING PURPOSE
Precision / Recall

CONNECT
Build on the preceding slide: The four kinds of result.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

POINT TO THE DEFINITION
Precision: Of all predicted warnings, the fraction that were actual warnings: TP / (TP + FP).
Recall: Of all actual warnings, the fraction detected: TP / (TP + FN).

NEXT
Precision and recall. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Precision and recall.

## Slide 12 — Precision and recall

PURPOSE
Precision and recall

CONNECT
Build on Precision / Recall. Explain why this example is needed before running it.

EXPLAIN
Precision asks: of the warnings raised, how many were correct?

Recall asks: of the real warnings, how many did we detect?

A zero denominator needs an explicit rule.

Use the rule in your task brief when implementing the function.

LECTURER DETAIL
TEACHING PURPOSE
Precision and recall

CONNECT
Build on the preceding slide: Precision / Recall.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Two fractions ask different questions. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Probability and a decision threshold.

## Slide 13 — Probability and a decision threshold

PURPOSE
Probability and a decision threshold

CONNECT
Build on Precision and recall. Explain why this example is needed before running it.

EXPLAIN
Probability: A probability is between 0 and 1. Multiply by 100 for percent: 0.7 is 70%. A model’s probability is an estimate that needs checking.
Threshold: A threshold turns a score into a decision. For a rule score >= 0.5, a score of 0.7 gives class 1. Use validation data to choose the threshold.

LECTURER DETAIL
TEACHING PURPOSE
Probability and a decision threshold

CONNECT
Build on the preceding slide: What the activity shows.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

POINT TO THE DEFINITION
Probability: A probability is between 0 and 1. Multiply by 100 for percent: 0.7 is 70%. A model’s probability is an estimate that needs checking.
Threshold: A threshold turns a score into a decision. For a rule score >= 0.5, a score of 0.7 gives class 1. Use validation data to choose the threshold.

NEXT
A category decision can use a probability. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A category decision can use a probability.

## Slide 14 — A category decision can use a probability

PURPOSE
A category decision can use a probability

CONNECT
Build on Probability and a decision threshold. Explain why this example is needed before running it.

EXPLAIN
A classifier may estimate the probability of class 1.

A threshold converts that estimate into warning or no warning.

Logistic regression is a classification model. Its probability estimates still need evaluation.

LECTURER DETAIL
TEACHING PURPOSE
A category decision can use a probability

CONNECT
Build on the preceding slide: Probability and a decision threshold.

LECTURER CUE
Only after the count exercise, show a classifier fit/predict demonstration. Logistic regression predicts a category despite its name. Probability estimates need not be well calibrated.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Probability and a warning decision. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Threshold and cost.

## Slide 15 — Threshold and cost

PURPOSE
Threshold and cost

CONNECT
Build on A category decision can use a probability. Explain why this example is needed before running it.

EXPLAIN
Threshold and cost: A threshold converts a score to a decision. A cost rule states how much each type of mistake matters. Lower thresholds usually increase recall; precision need not decrease at every step.

LECTURER DETAIL
TEACHING PURPOSE
Threshold and cost

CONNECT
Build on the preceding slide: Two fractions ask different questions.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

POINT TO THE DEFINITION
Threshold and cost: A threshold converts a score to a decision. A cost rule states how much each type of mistake matters. Lower thresholds usually increase recall; precision need not decrease at every step.

NEXT
State the cost rule before calculating. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
State the cost rule before calculating.

## Slide 16 — State the cost rule before calculating

PURPOSE
State the cost rule before calculating

CONNECT
Build on Threshold and cost. Explain why this example is needed before running it.

EXPLAIN
A cost rule assigns a penalty to each kind of mistake. In this teaching example, a missed warning costs 5 units and a false alarm costs 1 unit.

Total cost = 5 × FN + FP. One missed warning and one false alarm therefore cost 6 units.

These are invented teaching penalties. Use the published assignment cost rule and explain whose consequences it represents.

LECTURER DETAIL
TEACHING PURPOSE
State the cost rule before calculating

CONNECT
Build on the preceding slide: Threshold and cost.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
Counting syntax in the example. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting syntax in the example.

## Slide 17 — Counting syntax in the example

PURPOSE
Counting syntax in the example

CONNECT
Build on State the cost rule before calculating. Explain why this example is needed before running it.

EXPLAIN
Our paired lists must have matching lengths. zip alone stops at the shorter list.

LECTURER DETAIL
TEACHING PURPOSE
Counting syntax in the example

CONNECT
Build on the preceding slide: State the cost rule before calculating.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Worked example. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example.

## Slide 18 — Classification outcomes in Python

PURPOSE
Classification outcomes in Python

CONNECT
Build on Counting syntax in the example. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Worked example

CONNECT
Build on the preceding slide: Counting syntax in the example.

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

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
zip pairs items at matching positions in these equal-length lists.
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 19 — Classification outcomes results

PURPOSE
Classification outcomes results

CONNECT
Build on Classification outcomes in Python. Explain why this example is needed before running it.

EXPLAIN
Four paired rows, then precision 0.5, recall 0.5 and teaching cost 6.

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example.

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Counting arbitrary paired observations. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting arbitrary paired observations.

## Slide 20 — Counting arbitrary paired observations

PURPOSE
Counting arbitrary paired observations

CONNECT
Build on Classification outcomes results. Explain why this example is needed before running it.

EXPLAIN
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

tp = tn = fp = fn = 0 sets all four counters to zero. tp += 1 is shorthand for tp = tp + 1.

LECTURER DETAIL
TEACHING PURPOSE
Counting arbitrary paired observations

CONNECT
Build on the preceding slide: Expected output.

LECTURER CUE
Start every counter at zero before the loop. == compares labels. and means both comparisons must be true. elif checks another condition only when earlier ones were false.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Counting arbitrary paired observations in Python (1/3). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting arbitrary paired observations in Python (1/3).

## Slide 21 — Counting arbitrary paired observations in Python (1/3)

PURPOSE
Counting arbitrary paired observations in Python (1/3)

CONNECT
Build on Counting arbitrary paired observations. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Counting arbitrary paired observations in Python (1/3)

CONNECT
Build on the preceding slide: Counting arbitrary paired observations.

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

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

WALK THROUGH THIS CODE
= assigns the value on the right to the name on the left.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Counting arbitrary paired observations in Python (2/3). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting arbitrary paired observations in Python (2/3).

## Slide 22 — Counting arbitrary paired observations in Python (2/3)

PURPOSE
Counting arbitrary paired observations in Python (2/3)

CONNECT
Build on Counting arbitrary paired observations in Python (1/3). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Counting arbitrary paired observations in Python (2/3)

CONNECT
Build on the preceding slide: Counting arbitrary paired observations in Python (1/3).

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

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
zip pairs items at matching positions in these equal-length lists.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Counting arbitrary paired observations in Python (3/3). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Counting arbitrary paired observations in Python (3/3).

## Slide 23 — Counting arbitrary paired observations in Python (3/3)

PURPOSE
Counting arbitrary paired observations in Python (3/3)

CONNECT
Build on Counting arbitrary paired observations in Python (2/3). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Counting arbitrary paired observations in Python (3/3)

CONNECT
Build on the preceding slide: Counting arbitrary paired observations in Python (2/3).

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

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
You are the confusion matrix. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Represent a category with indicators.

## Slide 24 — Represent a category with indicators

PURPOSE
Represent a category with indicators

CONNECT
Build on Counting arbitrary paired observations in Python (3/3). Explain why this example is needed before running it.

EXPLAIN
Category: A category is a label such as steel or timber. Its name does not imply a numerical size or rank.
One-hot indicator: Create a column for each category. Its entry is 1 when the row has that category and 0 otherwise. Learn the allowed categories from training data.

LECTURER DETAIL
TEACHING PURPOSE
Represent a category with indicators

CONNECT
Build on the preceding slide: Probability and a warning decision.

EXPLAIN IN ORDINARY WORDS
A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.

CHECK AND EXPECTED ANSWER
Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.

IF LEARNERS ARE STUCK
Make two rows and two category columns by hand before showing the encoder.

POINT TO THE DEFINITION
Category: A category is a label such as steel or timber. Its name does not imply a numerical size or rank.
One-hot indicator: Create a column for each category. Its entry is 1 when the row has that category and 0 otherwise. Learn the allowed categories from training data.

NEXT
A category can become indicator columns. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A category can become indicator columns.

## Slide 25 — A category can become indicator columns

PURPOSE
A category can become indicator columns

CONNECT
Build on Represent a category with indicators. Explain why this example is needed before running it.

EXPLAIN
An encoder converts category labels to numeric columns. Fit it on training data. Each indicator is 1 when that category applies, otherwise 0.

LECTURER DETAIL
TEACHING PURPOSE
A category can become indicator columns

CONNECT
Build on the preceding slide: Represent a category with indicators.

LECTURER CUE
An indicator is 1 when its category applies and 0 otherwise. Fit the encoder on training data.

EXPLAIN IN ORDINARY WORDS
A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.

CHECK AND EXPECTED ANSWER
Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.

IF LEARNERS ARE STUCK
Make two rows and two category columns by hand before showing the encoder.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Accuracy can hide missed warnings. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Accuracy can hide missed warnings.

## Slide 26 — Accuracy can hide missed warnings

PURPOSE
Accuracy can hide missed warnings

CONNECT
Build on A category can become indicator columns. Explain why this example is needed before running it.

EXPLAIN
Accuracy = number of correct labels / number of labels. It counts correct warnings and correct non-warnings together.

If 90 of 100 cases need no warning, predicting no warning every time gives 90% accuracy. It detects none of the 10 real warnings: recall is 0.

Always inspect the actual/predicted counts and relevant costs before calling a classifier useful.

LECTURER DETAIL
TEACHING PURPOSE
Accuracy can hide missed warnings

CONNECT
Build on the preceding slide: A category can become indicator columns.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 27 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on Accuracy can hide missed warnings. Explain why this example is needed before running it.

EXPLAIN
Example: Change the second prediction to 1. Count again. Does this improve both recall and the assumed cost?

Answer: TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: Accuracy can hide missed warnings.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.
Which step produced this result? What changes if one input changes?
CML3113   Week 9   32
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 28 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
Implement classification_metrics on arbitrary paired binary labels, not only the example.

Use the published zero-denominator convention.

Read the supplied W09 comparison separately.

Teacher-written cost assumptions are not approved operating limits.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
Implement classification_metrics on arbitrary paired binary labels, not only the example. Use the published zero-denominator convention. Read the supplied W09 comparison separately. Teacher-written cost assumptions are not approved operating limits. All claimed benefits require real-world evaluation.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 29 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
All claimed benefits require real-world evaluation.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
Implement classification_metrics on arbitrary paired binary labels, not only the example. Use the published zero-denominator convention. Read the supplied W09 comparison separately. Teacher-written cost assumptions are not approved operating limits. All claimed benefits require real-world evaluation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Category predictions and operating thresholds. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Category predictions and operating thresholds.

## Slide 30 — Category predictions and operating thresholds

PURPOSE
Category predictions and operating thresholds

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
A majority-only classifier can achieve high accuracy while missing the rare class.

Name the positive class and both confusion-matrix axes.

A model expecting numeric features cannot directly use raw category strings; use numeric indicator columns for categories.

Compare threshold choices on validation data.

LECTURER DETAIL
TEACHING PURPOSE
Category predictions and operating thresholds

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Category predictions and operating thresholds continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Category predictions and operating thresholds continued.

## Slide 31 — Category predictions and operating thresholds continued

PURPOSE
Category predictions and operating thresholds continued

CONNECT
Build on Category predictions and operating thresholds. Explain why this example is needed before running it.

EXPLAIN
Reducing the threshold adds flagged cases and cannot reduce recall on fixed scored observations, but precision can move either way.

LECTURER DETAIL
TEACHING PURPOSE
Category predictions and operating thresholds continued

CONNECT
Build on the preceding slide: Category predictions and operating thresholds.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task.

## Slide 32 — Your issued task

PURPOSE
Your issued task

CONNECT
Build on Category predictions and operating thresholds continued. Explain why this example is needed before running it.

EXPLAIN
Use classification_case.csv.

Positive means a synthetic warning condition.

Compute the confusion matrix, precision, recall and cost.

Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Category predictions and operating thresholds continued.

LECTURER CUE
Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Your issued task continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task continued.

## Slide 33 — Your issued task continued

PURPOSE
Your issued task continued

CONNECT
Build on Your issued task. Explain why this example is needed before running it.

EXPLAIN
These costs are teaching assumptions, not approved operating limits.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task continued

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
classification_metrics(actual, predicted). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
classification_metrics(actual, predicted).

## Slide 34 — classification_metrics(actual, predicted)

PURPOSE
classification_metrics(actual, predicted)

CONNECT
Build on Your issued task continued. Explain why this example is needed before running it.

EXPLAIN
For binary labels return tp, tn, fp, fn, precision, recall and cost=5*fn+fp; use zero for an undefined precision/recall denominator.

LECTURER DETAIL
TEACHING PURPOSE
classification_metrics(actual, predicted)

CONNECT
Build on the preceding slide: Your issued task continued.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W09/CML3113/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Written evidence.

## Slide 35 — Written evidence

PURPOSE
Written evidence

CONNECT
Build on classification_metrics(actual, predicted). Explain why this example is needed before running it.

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER DETAIL
TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: classification_metrics(actual, predicted).

LECTURER CUE
Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Classification and cost submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Classification and cost submission.

## Slide 36 — Classification and cost submission

PURPOSE
Classification and cost submission

CONNECT
Build on Written evidence. Explain why this example is needed before running it.

EXPLAIN
Opens: 06 Nov 2026, 08:00 Kampala

Deadline: 13 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Classification and cost submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 9 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 9 quiz.

## Slide 37 — Week 9 quiz

PURPOSE
Week 9 quiz

CONNECT
Build on Classification and cost submission. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 9 quiz

CONNECT
Build on the preceding slide: Classification and cost submission.

LECTURER CUE
Activate the matching open_W9_CML3113 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 38 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 9 quiz. Explain why this example is needed before running it.

EXPLAIN
You can identify a false negative and explain precision and recall with counts.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 9 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Optional revision video.

## Slide 39 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals The Confusion Matrix

Opening up to 04:00, optional preview-selected excerpt

Listening question: Which observations are correctly or incorrectly classified?

LECTURER DETAIL
TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Translate the medical example to warning/no-warning and label the axes.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=Kdsp6soqA7o

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
