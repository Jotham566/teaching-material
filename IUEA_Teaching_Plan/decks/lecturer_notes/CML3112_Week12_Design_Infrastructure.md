# CML3112 Week12 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Choosing and explaining a model

PURPOSE
Choosing and explaining a model

CONNECT
Build on the preceding week. Explain why this example is needed before running it.

EXPLAIN
Civil Engineering and Architecture

LECTURER DETAIL
TEACHING PURPOSE
Choosing and explaining a model

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

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
Build on Choosing and explaining a model. Explain why this example is needed before running it.

EXPLAIN
Check model requirements before ranking candidates.

Apply the tie-break rule and explain the choice.

LECTURER DETAIL
TEACHING PURPOSE
Today’s learning

CONNECT
Build on the preceding slide: Choosing and explaining a model.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: A large grid search, four new model implementations and an adversarial defence are optional practice. They must not crowd out the core decision process.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

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
We already calculate validation errors. Now we combine those errors with a practical constraint and an explicit tie-break rule.

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
The lowest prediction error may come from a model that is too slow for the stated task. We apply the published constraints before ranking eligible models.

LECTURER DETAIL
TEACHING PURPOSE
The engineering context

CONNECT
Build on the preceding slide: Recall and a first attempt.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Constraint and Latency.

## Slide 5 — Constraint and Latency

PURPOSE
Constraint and Latency

CONNECT
Build on Why this week’s tools are needed. Explain why this example is needed before running it.

EXPLAIN
Constraint: A condition a candidate must satisfy, such as MAE at most 3 and latency at most 10 ms.
Latency: Time taken to produce a prediction under stated measurement conditions. Hardware and measurement method matter.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: The engineering context.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

POINT TO THE DEFINITION
Constraint: A condition a candidate must satisfy, such as MAE at most 3 and latency at most 10 ms.
Latency: Time taken to produce a prediction under stated measurement conditions. Hardware and measurement method matter.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Tie-break and Hyperparameter.

## Slide 6 — Tie-break and Hyperparameter

PURPOSE
Tie-break and Hyperparameter

CONNECT
Build on Constraint and Latency. Explain why this example is needed before running it.

EXPLAIN
Tie-break: A published rule for choosing between candidates that tie on the main criterion.
Hyperparameter: A setting chosen before fitting, such as tree depth. Tune using validation or cross-validation, not the final test.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

POINT TO THE DEFINITION
Tie-break: A published rule for choosing between candidates that tie on the main criterion.
Hyperparameter: A setting chosen before fitting, such as tree depth. Tune using validation or cross-validation, not the final test.

NEXT
Error and practical constraints. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Error and practical constraints.

## Slide 7 — Error and practical constraints

PURPOSE
Error and practical constraints

CONNECT
Build on Tie-break and Hyperparameter. Explain why this example is needed before running it.

EXPLAIN
A smaller error can require more computation.

A candidate must meet every stated requirement.

Compare eligible models on the same validation observations.

Follow the published tie-break rule when scores tie.

LECTURER DETAIL
TEACHING PURPOSE
Error and practical constraints

CONNECT
Build on the preceding slide: Words we will use.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

NEXT
A model comparison needs a fair test. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A model comparison needs a fair test.

## Slide 8 — A model comparison needs a fair test

PURPOSE
A model comparison needs a fair test

CONNECT
Build on Error and practical constraints. Explain why this example is needed before running it.

EXPLAIN
Use the same validation observations for every candidate.

Fit preprocessing on training data only.

Choose the error measure and practical requirements before inspecting results.

LECTURER DETAIL
TEACHING PURPOSE
A model comparison needs a fair test

CONNECT
Build on the preceding slide: Error and practical constraints.

LECTURER CUE
A tree asks successive questions. A forest combines many trees. More complexity does not guarantee better validation performance. The task’s tie-break rule remains authoritative.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Eligibility comes before ranking. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Eligibility comes before ranking.

## Slide 9 — Eligibility comes before ranking

PURPOSE
Eligibility comes before ranking

CONNECT
Build on A model comparison needs a fair test. Explain why this example is needed before running it.

EXPLAIN
First check every stated requirement for each candidate.

Reject a candidate that fails even one requirement.

Rank the eligible candidates using the published tie-break rule.

LECTURER DETAIL
TEACHING PURPOSE
Eligibility comes before ranking

CONNECT
Build on the preceding slide: A model comparison needs a fair test.

LECTURER CUE
Cross out ineligible candidates before ranking errors. Then apply the tie-break rule, rather than choosing the most sophisticated model.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

NEXT
A constrained model choice. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A constrained model choice.

## Slide 10 — A constrained model choice

PURPOSE
A constrained model choice

CONNECT
Build on Eligibility comes before ranking. Explain why this example is needed before running it.

EXPLAIN
Invented requirements: error at most 3 and time at most 10 ms.

LECTURER DETAIL
TEACHING PURPOSE
A constrained model choice

CONNECT
Build on the preceding slide: Eligibility comes before ranking.

LECTURER CUE
Invented requirements: error at most 3 and time at most 10 ms. Only simple is eligible. No result here is a measured engineering benchmark.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Worked example (1/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Candidate records and eligibility.

## Slide 11 — Candidate records and eligibility

PURPOSE
Candidate records and eligibility

CONNECT
Build on A constrained model choice. Explain why this example is needed before running it.

EXPLAIN
A candidate is one model under consideration. Its dictionary records a name, a validation error and measured run time.

An eligible candidate meets every published constraint. Build a list of eligible records first. If the list is empty, use the task’s specified no-candidate result.

LECTURER DETAIL


TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (1/2).

## Slide 12 — Model selection in Python (1/2)

PURPOSE
Model selection in Python (1/2)

CONNECT
Build on Candidate records and eligibility. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (1/2)

CONNECT
Build on the preceding slide: A constrained model choice.

LECTURER CUE
Cross out ineligible candidates before ranking errors. Then apply the tie-break rule, rather than choosing the most sophisticated model. Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection. A sorted list key can be a tuple: first metric, then speed, then name. Write a short recommendation: question, fair comparison, chosen candidate, reason, limitation and what new evidence could change the choice.

Complete practice code:
candidates = [{"name": "simple", "error": 3, "ms": 2},
              {"name": "complex", "error": 1, "ms": 20}]
eligible = []
for item in candidates:
    if item["error"] <= 3 and item["ms"] <= 10:
        eligible.append(item)
print([item["name"] for item in eligible])

WALK THROUGH THIS CODE
for takes the next item. The indented block repeats.
if tests a condition. The chosen indented block runs.
append adds one item to the end of a list.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Worked example (2/2). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Worked example (2/2).

## Slide 13 — Model selection in Python (2/2)

PURPOSE
Model selection in Python (2/2)

CONNECT
Build on Model selection in Python (1/2). Explain why this example is needed before running it.

EXPLAIN
Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER DETAIL
TEACHING PURPOSE
Worked example (2/2)

CONNECT
Build on the preceding slide: Worked example (1/2).

LECTURER CUE
Cross out ineligible candidates before ranking errors. Then apply the tie-break rule, rather than choosing the most sophisticated model. Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection. A sorted list key can be a tuple: first metric, then speed, then name. Write a short recommendation: question, fair comparison, chosen candidate, reason, limitation and what new evidence could change the choice.

Complete practice code:
candidates = [{"name": "simple", "error": 3, "ms": 2},
              {"name": "complex", "error": 1, "ms": 20}]
eligible = []
for item in candidates:
    if item["error"] <= 3 and item["ms"] <= 10:
        eligible.append(item)
print([item["name"] for item in eligible])

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

WALK THROUGH THIS CODE
print displays a value below the cell.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Expected output. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Expected output.

## Slide 14 — Model selection results

PURPOSE
Model selection results

CONNECT
Build on Model selection in Python (2/2). Explain why this example is needed before running it.

EXPLAIN
['simple']

LECTURER DETAIL
TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example (2/2).

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
A tuple supplies an ordered ranking key. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A tuple supplies an ordered ranking key.

## Slide 15 — A tuple supplies an ordered ranking key

PURPOSE
A tuple supplies an ordered ranking key

CONNECT
Build on Model selection results. Explain why this example is needed before running it.

EXPLAIN
A tuple holds several values in order, such as (error, time, name).

Python compares the first values. A tie moves the comparison to the second.

If those also tie, the third value decides.

LECTURER DETAIL
TEACHING PURPOSE
A tuple supplies an ordered ranking key

CONNECT
Build on the preceding slide: Expected output.

LECTURER CUE
Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection. A sorted list key can be a tuple: first metric, then speed, then name.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

NEXT
Sorting with a tie-break rule. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Sorting with a tie-break rule.

## Slide 16 — Sorting with a tie-break rule

PURPOSE
Sorting with a tie-break rule

CONNECT
Build on A tuple supplies an ordered ranking key. Explain why this example is needed before running it.

EXPLAIN
A tuple is an ordered group of values.

Python compares the first item, then the second when tied, then the third.

The key function gives sorted the tuple for each candidate.

Guard an empty list before selecting position zero.

LECTURER DETAIL
TEACHING PURPOSE
Sorting with a tie-break rule

CONNECT
Build on the preceding slide: A tuple supplies an ordered ranking key.

LECTURER CUE
A tuple is an ordered group of values. Python compares the first item, then the second when tied, then the third. The key function gives sorted the tuple for each candidate. Guard an empty list before selecting position zero.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

NEXT
Sorting with a named function. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Sorting with a named function.

## Slide 17 — Sorting with a named function

PURPOSE
Sorting with a named function

CONNECT
Build on Sorting with a tie-break rule. Explain why this example is needed before running it.

EXPLAIN
Check for an empty list before accessing position zero.

LECTURER DETAIL
TEACHING PURPOSE
Sorting with a named function

CONNECT
Build on the preceding slide: Sorting with a tie-break rule.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Sorting with a tie-break rule in Python. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Sorting with a tie-break rule in Python.

## Slide 18 — Sorting with a tie-break rule in Python

PURPOSE
Sorting with a tie-break rule in Python

CONNECT
Build on Sorting with a named function. Explain why this example is needed before running it.

EXPLAIN
Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER DETAIL
TEACHING PURPOSE
Sorting with a tie-break rule in Python

CONNECT
Build on the preceding slide: Sorting with a named function.

LECTURER CUE
A tuple is an ordered group of values. Python compares the first item, then the second when tied, then the third. The key function gives sorted the tuple for each candidate. Guard an empty list before selecting position zero.

Complete practice code:
def rank(item):
    return (item["error"], item["ms"], item["name"])

ordered = sorted(eligible, key=rank)
if len(ordered) == 0:
    winner = None
else:
    winner = ordered[0]["name"]
print(winner)

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

WALK THROUGH THIS CODE
def names the function. Inputs go inside parentheses.
if tests a condition. The chosen indented block runs.
return sends the result back to the caller.
Read the displayed lines in order, with the preceding code block if this example continues. Ask for the next value before running. The complete matching example is in guided_practice.ipynb; do not type a fragment into a new empty notebook.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Local explanation and Conditions of use.

## Slide 19 — Local explanation and Conditions of use

PURPOSE
Local explanation and Conditions of use

CONNECT
Build on Sorting with a tie-break rule in Python. Explain why this example is needed before running it.

EXPLAIN
Local explanation: Why a model made one particular prediction. This is different from global importance, which summarises behaviour over many cases.
Conditions of use: The cases and operating circumstances for which the available evidence supports considering the model.

LECTURER DETAIL
TEACHING PURPOSE
Words we will use

CONNECT
Build on the preceding slide: Sorting with a tie-break rule in Python.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

POINT TO THE DEFINITION
Local explanation: Why a model made one particular prediction. This is different from global importance, which summarises behaviour over many cases.
Conditions of use: The cases and operating circumstances for which the available evidence supports considering the model.

NEXT
A recommendation needs evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
A recommendation needs evidence.

## Slide 20 — A recommendation needs evidence

PURPOSE
A recommendation needs evidence

CONNECT
Build on Local explanation and Conditions of use. Explain why this example is needed before running it.

EXPLAIN
State the question and the chosen candidate.

Give the evaluation result and the constraint it satisfies.

State a limitation and the evidence that could change the recommendation.

LECTURER DETAIL
TEACHING PURPOSE
A recommendation needs evidence

CONNECT
Build on the preceding slide: Words we will use.

LECTURER CUE
Write a short recommendation: question, fair comparison, chosen candidate, reason, limitation and what new evidence could change the choice.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
You are the model selector. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Revision example and answer.

## Slide 21 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Build on A recommendation needs evidence. Explain why this example is needed before running it.

EXPLAIN
Example: A third model has error 3 and latency 1 ms. Under lowest error then lowest latency, which eligible model wins?

Answer: The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

LECTURER DETAIL
TEACHING PURPOSE
Your turn

CONNECT
Build on the preceding slide: What the activity shows.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

DISCUSSION KEY FOR THIS SLIDE
DISCUSS THE REASONING
Practice discussion
The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.
Which step produced this result? What changes if one input changes?
CML3112   Week 12   23
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
Practice discussion. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment.

## Slide 22 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Build on Revision example and answer. Explain why this example is needed before running it.

EXPLAIN
W12 uses fields name, validation_mae and latency_ms.

Meet both inclusive constraints, then rank by error, latency and alphabetical name.

Return None if no candidate qualifies.

Complete the error function and interpret the separately supplied scenario.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment

CONNECT
Build on the preceding slide: After the video.

LECTURER CUE
W12 uses fields name, validation_mae and latency_ms. Meet both inclusive constraints, then rank by error, latency and alphabetical name. Return None if no candidate qualifies. Complete the error function and interpret the separately supplied scenario. Keep project comparisons and graded interfaces distinct.

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Preparing for the assignment continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Preparing for the assignment continued.

## Slide 23 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Build on Preparing for the assignment. Explain why this example is needed before running it.

EXPLAIN
Keep project comparisons and graded interfaces distinct.

LECTURER DETAIL
TEACHING PURPOSE
Preparing for the assignment continued

CONNECT
Build on the preceding slide: Preparing for the assignment.

LECTURER CUE
W12 uses fields name, validation_mae and latency_ms. Meet both inclusive constraints, then rank by error, latency and alphabetical name. Return None if no candidate qualifies. Complete the error function and interpret the separately supplied scenario. Keep project comparisons and graded interfaces distinct.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Fair comparison and explanation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Fair comparison and explanation.

## Slide 24 — Fair comparison and explanation

PURPOSE
Fair comparison and explanation

CONNECT
Build on Preparing for the assignment continued. Explain why this example is needed before running it.

EXPLAIN
Compare the same metric on the same validation cases with the same preprocessing rules.

A small difference needs context, including variation across splits.

Code run out of order can overwrite the variable holding a model; restart and run from the top.

A local explanation addresses one prediction; global importance summarises many.

LECTURER DETAIL
TEACHING PURPOSE
Fair comparison and explanation

CONNECT
Build on the preceding slide: Preparing for the assignment continued.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Fair comparison and explanation continued. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Fair comparison and explanation continued.

## Slide 25 — Fair comparison and explanation continued

PURPOSE
Fair comparison and explanation continued

CONNECT
Build on Fair comparison and explanation. Explain why this example is needed before running it.

EXPLAIN
A post-hoc explanation of a complex model is not its directly readable internal rule.

LECTURER DETAIL
TEACHING PURPOSE
Fair comparison and explanation continued

CONNECT
Build on the preceding slide: Fair comparison and explanation.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Your issued task. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Your issued task.

## Slide 26 — Your issued task

PURPOSE
Your issued task

CONNECT
Build on Fair comparison and explanation continued. Explain why this example is needed before running it.

EXPLAIN
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER DETAIL
TEACHING PURPOSE
Your issued task

CONNECT
Build on the preceding slide: Fair comparison and explanation continued.

LECTURER CUE
Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
select_model(candidates, max_mae, max_ms). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
select_model(candidates, max_mae, max_ms).

## Slide 27 — select_model(candidates, max_mae, max_ms)

PURPOSE
select_model(candidates, max_mae, max_ms)

CONNECT
Build on Your issued task. Explain why this example is needed before running it.

EXPLAIN
Candidates have name, validation_mae and latency_ms.

Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.

Return the selected name or None.

Never use test scores for selection.

LECTURER DETAIL
TEACHING PURPOSE
select_model(candidates, max_mae, max_ms)

CONNECT
Build on the preceding slide: Your issued task.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W12/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
regression_errors(actual, predicted). Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
regression_errors(actual, predicted).

## Slide 28 — regression_errors(actual, predicted)

PURPOSE
regression_errors(actual, predicted)

CONNECT
Build on select_model(candidates, max_mae, max_ms). Explain why this example is needed before running it.

EXPLAIN
Return mae and rmse, calculated over the same paired observations, with full precision.

LECTURER DETAIL
TEACHING PURPOSE
regression_errors(actual, predicted)

CONNECT
Build on the preceding slide: select_model(candidates, max_mae, max_ms).

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W12/CML3112/A/TASKS.md

EXPLAIN IN ORDINARY WORDS
An error compares prediction with measured truth. Absolute error ignores direction. MAE averages absolute errors; RMSE squares, averages, then takes a square root. Both use the target unit.

CHECK AND EXPECTED ANSWER
Actual [4,8], predicted [5,6]: prediction-minus-actual errors [1,-2], MAE=1.5, RMSE=sqrt(2.5), about 1.58.

IF LEARNERS ARE STUCK
Calculate one pair by hand first. For signed percentage error follow the precise sign convention in the issued task.

NEXT
Written evidence. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Written evidence.

## Slide 29 — Written evidence

PURPOSE
Written evidence

CONNECT
Build on regression_errors(actual, predicted). Explain why this example is needed before running it.

EXPLAIN
Use the cell headed “My written evidence”.

Explain the supplied scenario in your own words.

State target units, reasons and limitations.

Submit one complete notebook containing code and written evidence.

LECTURER DETAIL
TEACHING PURPOSE
Written evidence

CONNECT
Build on the preceding slide: regression_errors(actual, predicted).

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
Model recommendation submission. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Model recommendation submission.

## Slide 30 — Model recommendation submission

PURPOSE
Model recommendation submission

CONNECT
Build on Written evidence. Explain why this example is needed before running it.

EXPLAIN
Opens: 24 Nov 2026, 11:00 Kampala

Deadline: 24 Nov 2026, 14:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER DETAIL
TEACHING PURPOSE
Model recommendation submission

CONNECT
Build on the preceding slide: Written evidence.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Project preparation. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Project preparation.

## Slide 31 — Project preparation

PURPOSE
Project preparation

CONNECT
Build on Model recommendation submission. Explain why this example is needed before running it.

EXPLAIN
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 15 Dec 2026, 11:00 Kampala

LECTURER DETAIL
TEACHING PURPOSE
Project preparation

CONNECT
Build on the preceding slide: Model recommendation submission.

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
Week 12 quiz. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Week 12 quiz.

## Slide 32 — Week 12 quiz

PURPOSE
Week 12 quiz

CONNECT
Build on Project preparation. Explain why this example is needed before running it.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER DETAIL
TEACHING PURPOSE
Week 12 quiz

CONNECT
Build on the preceding slide: Project preparation.

LECTURER CUE
Activate the matching open_W12_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
Before you leave. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Before you leave.

## Slide 33 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Build on Week 12 quiz. Explain why this example is needed before running it.

EXPLAIN
You can justify a valid candidate with evidence and a stated limitation.

Save your work and check the required submission files.

LECTURER DETAIL
TEACHING PURPOSE
Before you leave

CONNECT
Build on the preceding slide: Week 12 quiz.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
Optional revision video.

## Slide 34 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Build on Revision and submission checklist. Explain why this example is needed before running it.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

LECTURER DETAIL
TEACHING PURPOSE
Short explainer and discussion

CONNECT
Build on the preceding slide: Practice discussion.

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Explain why our repeated equipment IDs require grouped partitions rather than ordinary random folds.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fSytzGwwBVw

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
After the video. Move on after a learner can explain the current example or required action.

TEACHING MODE
Demonstrate the example directly. Explain each new name, symbol and output. Use the revision example for an individual check after class; no live partner activity is required.

NEXT
independent revision and the issued task.
