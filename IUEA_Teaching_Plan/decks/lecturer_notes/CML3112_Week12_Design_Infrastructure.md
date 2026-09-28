# CML3112 Week12 Design Infrastructure

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Choosing and explaining a model

PURPOSE
Choosing and explaining a model

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
Previous slide: Choosing and explaining a model.

EXPLAIN
Check model requirements before ranking candidates.

Apply the tie-break rule and explain the choice.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: A large grid search, four new model implementations and an adversarial defence are optional practice. They must not crowd out the core decision process.

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
We already calculate validation errors. Now we combine those errors with a practical constraint and an explicit tie-break rule.

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
The lowest prediction error may come from a model that is too slow for the stated task. We apply the published constraints before ranking eligible models.

LECTURER CUE
A building team records indoor temperature to investigate comfort. Civil students can discuss construction and inspection; architecture students can discuss shading and ventilation. Explain the quantities before using them.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Constraint and Latency.

REFERENCES


## Slide 5 — Constraint and Latency

PURPOSE
Constraint and Latency

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
Constraint: A condition a candidate must satisfy, such as MAE at most 3 and latency at most 10 ms.

Latency: Time taken to produce a prediction under stated measurement conditions. Hardware and measurement method matter.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Tie-break and Hyperparameter.

REFERENCES


## Slide 6 — Tie-break and Hyperparameter

PURPOSE
Tie-break and Hyperparameter

CONNECT
Previous slide: Constraint and Latency.

EXPLAIN
Tie-break: A published rule for choosing between candidates that tie on the main criterion.

Hyperparameter: A setting chosen before fitting, such as tree depth. Tune using validation or cross-validation, not the final test.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Error and practical constraints.

REFERENCES


## Slide 7 — Error and practical constraints

PURPOSE
Error and practical constraints

CONNECT
Previous slide: Tie-break and Hyperparameter.

EXPLAIN
A smaller error can require more computation.

A candidate must meet every stated requirement.

Compare eligible models on the same validation observations.

Follow the published tie-break rule when scores tie.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A model comparison needs a fair test.

REFERENCES


## Slide 8 — A model comparison needs a fair test

PURPOSE
A model comparison needs a fair test

CONNECT
Previous slide: Error and practical constraints.

EXPLAIN
Use the same validation observations for every candidate.

Fit preprocessing on training data only.

Choose the error measure and practical requirements before inspecting results.

LECTURER CUE
A tree asks successive questions. A forest combines many trees. More complexity does not guarantee better validation performance. The task’s tie-break rule remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Eligibility comes before ranking.

REFERENCES


## Slide 9 — Eligibility comes before ranking

PURPOSE
Eligibility comes before ranking

CONNECT
Previous slide: A model comparison needs a fair test.

EXPLAIN
First check every stated requirement for each candidate.

Reject a candidate that fails even one requirement.

Rank the eligible candidates using the published tie-break rule.

LECTURER CUE
Cross out ineligible candidates before ranking errors. Then apply the tie-break rule, rather than choosing the most sophisticated model.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A constrained model choice.

REFERENCES


## Slide 10 — A constrained model choice

PURPOSE
A constrained model choice

CONNECT
Previous slide: Eligibility comes before ranking.

EXPLAIN
Candidate | Validation error | Time (ms)

simple | 3 | 2

complex | 1 | 20

Invented requirements: error at most 3 and time at most 10 ms.

LECTURER CUE
Invented requirements: error at most 3 and time at most 10 ms. Only simple is eligible. No result here is a measured engineering benchmark.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Candidate records and eligibility.

REFERENCES


## Slide 11 — Candidate records and eligibility

PURPOSE
Candidate records and eligibility

CONNECT
Previous slide: A constrained model choice.

EXPLAIN
A candidate is one model under consideration. Its dictionary records a name, a validation error and measured run time.

An eligible candidate meets every published constraint. Build a list of eligible records first. If the list is empty, use the task’s specified no-candidate result.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (1/2).

REFERENCES


## Slide 12 — Model selection in Python (1/2)

PURPOSE
Model selection in Python (1/2)

CONNECT
Previous slide: Candidate records and eligibility.

EXPLAIN
Read the code in this order:
candidates = [{"name": "simple", "error": 3, "ms": 2},
              {"name": "complex", "error": 1, "ms": 20}]
eligible = []
for item in candidates:
    if item["error"] <= 3 and item["ms"] <= 10:
        eligible.append(item)
names = []
for item in eligible:
    names.append(item["name"])

for takes the next item. The indented block repeats.

if tests a condition. The chosen indented block runs.

append adds one item to the end of a list.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example (2/2).

REFERENCES


## Slide 13 — Model selection in Python (2/2)

PURPOSE
Model selection in Python (2/2)

CONNECT
Previous slide: Model selection in Python (1/2).

EXPLAIN
Read the code in this order:
print(names)

print displays a value below the cell.

Continue the SAME cell; keep indentation. Run after all parts are entered.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 14 — Model selection results

PURPOSE
Model selection results

CONNECT
Previous slide: Model selection in Python (2/2).

EXPLAIN
['simple']

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A tuple supplies an ordered ranking key.

REFERENCES


## Slide 15 — A tuple supplies an ordered ranking key

PURPOSE
A tuple supplies an ordered ranking key

CONNECT
Previous slide: Model selection results.

EXPLAIN
A tuple holds several values in order, such as (error, time, name).

Python compares the first values. A tie moves the comparison to the second.

If those also tie, the third value decides.

LECTURER CUE
Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection. A sorted list key can be a tuple: first metric, then speed, then name.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace a tuple ranking key.

REFERENCES


## Slide 16 — Trace a tuple ranking key

PURPOSE
Trace a tuple ranking key

CONNECT
Previous slide: A tuple supplies an ordered ranking key.

EXPLAIN
Candidate | Key: error, ms, name | Position

beta | (2, 5, "beta") | 1: lower error

alpha | (3, 1, "alpha") | 2: tie on error; faster

gamma | (3, 2, "gamma") | 3: same error; slower

Only eligible candidates reach ranking. If error and time tie, compare the names alphabetically.

Read the rows in order. Only eligible candidates reach ranking. If error and time tie, compare the names alphabetically.

Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Pass a function as the sorting key.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 17 — Pass a function as the sorting key

PURPOSE
Pass a function as the sorting key

CONNECT
Previous slide: Trace a tuple ranking key.

EXPLAIN
sorted returns a new list in order. In sorted(eligible, key=rank), rank is the function itself, passed without calling it.

sorted calls rank(item) for each candidate and compares the returned tuples. Writing rank() here would call it immediately without its required input.

The original eligible list is unchanged. Check len(ordered) before using ordered[0], because an empty list has no first position.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Sorting with a tie-break rule.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 18 — Sorting with a tie-break rule

PURPOSE
Sorting with a tie-break rule

CONNECT
Previous slide: Pass a function as the sorting key.

EXPLAIN
A tuple is an ordered group of values.

Python compares the first item, then the second when tied, then the third.

The key function gives sorted the tuple for each candidate.

Guard an empty list before selecting position zero.

LECTURER CUE
A tuple is an ordered group of values. Python compares the first item, then the second when tied, then the third. The key function gives sorted the tuple for each candidate. Guard an empty list before selecting position zero.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Sorting with a named function.

REFERENCES


## Slide 19 — Sorting with a named function

PURPOSE
Sorting with a named function

CONNECT
Previous slide: Sorting with a tie-break rule.

EXPLAIN
Expression | Meaning

key=rank | Use rank to build each comparison key

sorted(eligible, key=rank) | Return a newly ordered list

ordered[0] | Select its first item

len(ordered) == 0 | Check for no eligible candidate

Check for an empty list before accessing position zero.

LECTURER CUE
Read one row at a time and use a changed value. This is a syntax reference for the worked examples.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Sorting with a tie-break rule in Python.

REFERENCES


## Slide 20 — Sorting with a tie-break rule in Python

PURPOSE
Sorting with a tie-break rule in Python

CONNECT
Previous slide: Sorting with a named function.

EXPLAIN
Read the code in this order:
def rank(item):
    return (item["error"], item["ms"], item["name"])

ordered = sorted(eligible, key=rank)
if len(ordered) == 0:
    winner = None
else:
    winner = ordered[0]["name"]
print(winner)

def names the function. Inputs go inside parentheses.

if tests a condition. The chosen indented block runs.

return sends the result back to the caller.

Read top to bottom. Run the complete example in the matching practice notebook.

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

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Local explanation and Conditions of use.

REFERENCES


## Slide 21 — Local explanation and Conditions of use

PURPOSE
Local explanation and Conditions of use

CONNECT
Previous slide: Sorting with a tie-break rule in Python.

EXPLAIN
Local explanation: Why a model made one particular prediction. This is different from global importance, which summarises behaviour over many cases.

Conditions of use: The cases and operating circumstances for which the available evidence supports considering the model.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A recommendation needs evidence.

REFERENCES


## Slide 22 — A recommendation needs evidence

PURPOSE
A recommendation needs evidence

CONNECT
Previous slide: Local explanation and Conditions of use.

EXPLAIN
State the question and the chosen candidate.

Give the evaluation result and the constraint it satisfies.

State a limitation and the evidence that could change the recommendation.

LECTURER CUE
Write a short recommendation: question, fair comparison, chosen candidate, reason, limitation and what new evidence could change the choice.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 23 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: A recommendation needs evidence.

EXPLAIN
Example: A third model has error 3 and latency 1 ms. Under lowest error then lowest latency, which eligible model wins?

Answer: The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 24 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
W12 uses fields name, validation_mae and latency_ms.

Meet both inclusive constraints, then rank by error, latency and alphabetical name.

Return None if no candidate qualifies.

Complete the error function and interpret the separately supplied scenario.

LECTURER CUE
W12 uses fields name, validation_mae and latency_ms. Meet both inclusive constraints, then rank by error, latency and alphabetical name. Return None if no candidate qualifies. Complete the error function and interpret the separately supplied scenario. Keep project comparisons and graded interfaces distinct.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment continued.

REFERENCES


## Slide 25 — Preparing for the assignment continued

PURPOSE
Preparing for the assignment continued

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
Keep project comparisons and graded interfaces distinct.

LECTURER CUE
W12 uses fields name, validation_mae and latency_ms. Meet both inclusive constraints, then rank by error, latency and alphabetical name. Return None if no candidate qualifies. Complete the error function and interpret the separately supplied scenario. Keep project comparisons and graded interfaces distinct.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Fair comparison and explanation.

REFERENCES


## Slide 26 — Fair comparison and explanation

PURPOSE
Fair comparison and explanation

CONNECT
Previous slide: Preparing for the assignment continued.

EXPLAIN
Compare the same metric on the same validation cases with the same preprocessing rules.

A small difference needs context, including variation across splits.

Code run out of order can overwrite the variable holding a model; restart and run from the top.

A local explanation addresses one prediction; global importance summarises many.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Fair comparison and explanation continued.

REFERENCES


## Slide 27 — Fair comparison and explanation continued

PURPOSE
Fair comparison and explanation continued

CONNECT
Previous slide: Fair comparison and explanation.

EXPLAIN
A post-hoc explanation of a complex model is not its directly readable internal rule.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Your issued task.

REFERENCES


## Slide 28 — Your issued task

PURPOSE
Your issued task

CONNECT
Previous slide: Fair comparison and explanation continued.

EXPLAIN
Investigate building cooling load.

Target units: kW.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER CUE
Investigate building cooling load. Target units: kW. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
select_model(candidates, max_mae, max_ms).

REFERENCES


## Slide 29 — select_model(candidates, max_mae, max_ms)

PURPOSE
select_model(candidates, max_mae, max_ms)

CONNECT
Previous slide: Your issued task.

EXPLAIN
Candidates have name, validation_mae and latency_ms.

Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.

Return the selected name or None.

Never use test scores for selection.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W12/CML3112/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
regression_errors(actual, predicted).

REFERENCES


## Slide 30 — regression_errors(actual, predicted)

PURPOSE
regression_errors(actual, predicted)

CONNECT
Previous slide: select_model(candidates, max_mae, max_ms).

EXPLAIN
Return mae and rmse, calculated over the same paired observations, with full precision.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W12/CML3112/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 31 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: regression_errors(actual, predicted).

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
Model recommendation submission.

REFERENCES


## Slide 32 — Model recommendation submission

PURPOSE
Model recommendation submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 24 Nov 2026, 11:00 Kampala

Deadline: 24 Nov 2026, 14:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

LECTURER CUE
The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Project preparation.

REFERENCES


## Slide 33 — Project preparation

PURPOSE
Project preparation

CONNECT
Previous slide: Model recommendation submission.

EXPLAIN
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 15 Dec 2026, 11:00 Kampala

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 12 quiz.

REFERENCES


## Slide 34 — Week 12 quiz

PURPOSE
Week 12 quiz

CONNECT
Previous slide: Project preparation.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W12_CML3112 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 35 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 12 quiz.

EXPLAIN
You can justify a valid candidate with evidence and a stated limitation.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Optional revision video.

REFERENCES


## Slide 36 — Optional revision video

PURPOSE
Optional revision video

CONNECT
Previous slide: Revision and submission checklist.

EXPLAIN
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

LECTURER CUE
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.
After viewing: Explain why our repeated equipment IDs require grouped partitions rather than ordinary random folds.
Preview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: https://www.youtube.com/watch?v=fSytzGwwBVw

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
