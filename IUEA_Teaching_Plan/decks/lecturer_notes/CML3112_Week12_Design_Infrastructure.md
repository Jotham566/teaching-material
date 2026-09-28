# CML3112 Week12 Design Infrastructure

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Choosing and explaining a model

TEACHING PURPOSE
Choosing and explaining a model

LECTURER CUE
Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload.

NEXT
Today’s learning. Move on after a learner can explain the current example or required action.

## Slide 2 — Today’s learning

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

## Slide 3 — Recall and a first attempt

TEACHING PURPOSE
Recall and a first attempt

CONNECT
Build on the preceding slide: Today’s learning.

LECTURER CUE
Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: Students justify a valid simple model over a more accurate but ineligible one, and distinguish local explanation from global importance.

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
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

EXPLAIN IN ORDINARY WORDS
A calculated column stores a result for each row at refresh. A measure is evaluated under the filters of the current visual. SUMX evaluates an expression for each row before adding it.

CHECK AND EXPECTED ANSWER
Should revenue respond to a selected region? Yes; test the measure with that filter and reconcile it to known data.

IF LEARNERS ARE STUCK
Work one order line by hand, then two lines. Name the numerator and denominator populations before an average-order-value measure.

NEXT
Words we will use. Move on after a learner can explain the current example or required action.

## Slide 5 — Words we will use

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

## Slide 6 — Words we will use

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

## Slide 7 — Error and practical constraints

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

## Slide 8 — A model comparison needs a fair test

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

## Slide 9 — Eligibility comes before ranking

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

## Slide 10 — A constrained model choice

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

## Slide 11 — Worked example (1/2)

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

## Slide 12 — Worked example (2/2)

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

## Slide 13 — Expected output

TEACHING PURPOSE
Expected output

CONNECT
Build on the preceding slide: Worked example (2/2).

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

NEXT
A tuple supplies an ordered ranking key. Move on after a learner can explain the current example or required action.

## Slide 14 — A tuple supplies an ordered ranking key

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

## Slide 15 — Sorting with a tie-break rule

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

## Slide 16 — Sorting with a named function

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

## Slide 17 — Sorting with a tie-break rule in Python

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

## Slide 18 — Words we will use

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

## Slide 19 — A recommendation needs evidence

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

## Slide 20 — You are the model selector

TEACHING PURPOSE
You are the model selector

CONNECT
Build on the preceding slide: A recommendation needs evidence.

LECTURER CUE
Do this before revealing the discussion slide. One learner moves or writes the items, the other checks. Swap roles. Every student explains one step. Expected: B fails the time limit. A and C tie on error. C wins because 1 ms is lower than 2 ms.
Wait for an individual prediction before inviting pair discussion. Give a first-step hint if needed.

EXPLAIN IN ORDINARY WORDS
First remove models that fail the stated error or speed limits. Then apply the stated ranking and tie-break rules to eligible models. The smallest error alone need not decide.

CHECK AND EXPECTED ANSWER
If a model has the lowest error but exceeds the maximum latency, is it eligible? No.

IF LEARNERS ARE STUCK
Write an eligibility column and a separate ranking column. Check the exact boundary rule before sorting.

NEXT
What the activity shows. Move on after a learner can explain the current example or required action.

## Slide 21 — What the activity shows

TEACHING PURPOSE
What the activity shows

CONNECT
Build on the preceding slide: You are the model selector.

LECTURER CUE
Ask which step produced this answer. Return to the concrete action if a learner cannot explain it. This is practice feedback, never a quiz key.

NEXT
Your turn. Move on after a learner can explain the current example or required action.

## Slide 22 — Your turn

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

## Slide 23 — Practice discussion

TEACHING PURPOSE
Practice discussion

CONNECT
Build on the preceding slide: Your turn.

LECTURER CUE
Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.

NEXT
Short explainer and discussion. Move on after a learner can explain the current example or required action.

## Slide 24 — Short explainer and discussion

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

## Slide 25 — After the video

TEACHING PURPOSE
After the video

CONNECT
Build on the preceding slide: Short explainer and discussion.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

NEXT
Preparing for the assignment. Move on after a learner can explain the current example or required action.

## Slide 26 — Preparing for the assignment

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

## Slide 27 — Preparing for the assignment continued

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

## Slide 28 — Fair comparison and explanation

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

## Slide 29 — Fair comparison and explanation continued

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

## Slide 30 — Your issued task

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

## Slide 31 — select_model(candidates, max_mae, max_ms)

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

## Slide 32 — regression_errors(actual, predicted)

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

## Slide 33 — Written evidence

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

## Slide 34 — Model recommendation submission

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

## Slide 35 — Project preparation

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

## Slide 36 — Week 12 quiz

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

## Slide 37 — Before you leave

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

