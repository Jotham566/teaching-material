# CML3113 Week09 Mining Petroleum

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Classification and the cost of mistakes

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

## Slide 2 — Today’s learning

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

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Ask students to explain a false negative in their own programme and identify the denominator of recall.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
The engineering context. Move on after a learner can explain the current example or required action.

## Slide 4 — The engineering context

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

## Slide 5 — The positive class

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

## Slide 6 — Class and positive label / TP and TN

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

## Slide 7 — FP and FN

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

## Slide 8 — Actual and predicted describe different things

TEACHING PURPOSE
Actual and predicted describe different things

CONNECT
Build on the preceding slide: FP and FN.

LECTURER CUE
Place four paper observations in a table of actual label and predicted label. Classify each before showing the four-cell matrix. State which axis is actual and which is predicted.

NEXT
Every paired result belongs in one cell. Move on after a learner can explain the current example or required action.

## Slide 9 — Every paired result belongs in one cell

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

## Slide 10 — The four kinds of result

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

## Slide 11 — Precision / Recall

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

## Slide 12 — Precision and recall

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

## Slide 13 — Two fractions ask different questions

TEACHING PURPOSE
Two fractions ask different questions

CONNECT
Build on the preceding slide: Precision and recall.

LECTURER CUE
Use counts before fractions. The denominator of precision is predicted positives; the denominator of recall is actual positives. Explain what happens if either denominator is zero.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Threshold and cost. Move on after a learner can explain the current example or required action.

## Slide 14 — Threshold and cost

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

## Slide 15 — State the cost rule before calculating

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

## Slide 16 — Counting syntax in the example

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

## Slide 17 — Worked example

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

## Slide 18 — Expected output

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

## Slide 19 — Counting arbitrary paired observations

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

## Slide 20 — Counting arbitrary paired observations in Python (1/3)

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

## Slide 21 — Counting arbitrary paired observations in Python (2/3)

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

## Slide 22 — Counting arbitrary paired observations in Python (3/3)

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

## Slide 23 — You are the confusion matrix

TEACHING PURPOSE
You are the confusion matrix

CONNECT
Build on the preceding slide: Counting arbitrary paired observations in Python (3/3).

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: Each cell contains one card. Precision = 1 / 2 and recall = 1 / 2. The denominators count different sets of warnings.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 24 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the confusion matrix.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Probability and a decision threshold. Move on after a learner can explain the current example or required action.

## Slide 25 — Probability and a decision threshold

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

## Slide 26 — A category decision can use a probability

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

## Slide 27 — Probability and a warning decision

TEACHING PURPOSE
Probability and a warning decision

CONNECT
Build on the preceding slide: A category decision can use a probability.

LECTURER CUE
Lowering a threshold on fixed predictions cannot reduce the number flagged. Precision may rise or fall. Evaluate costs using validation data.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Represent a category with indicators. Move on after a learner can explain the current example or required action.

## Slide 28 — Represent a category with indicators

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

## Slide 29 — A category can become indicator columns

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

## Slide 30 — Accuracy can hide missed warnings

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

## Slide 31 — Your turn

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

## Slide 32 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

EXPLAIN IN ORDINARY WORDS
Name the positive class first. Actual is what happened; predicted is the model decision. Precision asks how many predicted positives were right. Recall asks how many actual positives were found.

CHECK AND EXPECTED ANSWER
With TP=2, FP=1, FN=2: precision=2/3 and recall=2/4. A missed actual positive is a false negative.

IF LEARNERS ARE STUCK
Draw actual/predicted headings. Place one case at a time before calculating a fraction. Explain the task rule for a zero denominator.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 33 — Short explainer and discussion

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

## Slide 34 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 35 — Preparing for the assignment

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

## Slide 36 — Preparing for the assignment continued

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

## Slide 37 — Category predictions and operating thresholds

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

## Slide 38 — Category predictions and operating thresholds continued

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

## Slide 39 — Your issued task

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

## Slide 40 — Your issued task continued

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

## Slide 41 — classification_metrics(actual, predicted)

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

## Slide 42 — Written evidence

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

## Slide 43 — Classification and cost submission

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

## Slide 44 — Week 9 quiz

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

## Slide 45 — Before you leave

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

