# CML3111 Week12 Engineering

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Choosing and explaining a model

Choosing and explaining a model
CML3111, Week 12, slide 1

Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Communications, Electrical, Mechatronics and Robotics Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3111, Week 12, slide 2

Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Check model requirements before ranking candidates.

Apply the tie-break rule and explain the choice.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3111, Week 12, slide 3

Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
We already calculate validation errors. Now we combine those errors with a practical constraint and an explicit tie-break rule.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3111, Week 12, slide 4

Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
The lowest prediction error may come from a model that is too slow for the stated task. We apply the published constraints before ranking eligible models.

Continue to
Constraint and Latency

## Slide 5 — Constraint and Latency

Constraint and Latency
CML3111, Week 12, slide 5

Explanation to give
Separate eligibility from ranking. A model that violates a required error or latency limit cannot win merely because another score is attractive. Latency is time per prediction in the stated measurement setting.

Worked illustration / lecturer answer
With limits MAE <= 5 and latency <= 10 ms, a candidate at MAE 4 and 12 ms fails eligibility. A candidate at MAE 5 and 10 ms passes inclusive limits.

Misconception to address
Establish units and whether boundaries are inclusive. An error of 4 is not comparable across different target units or evaluation samples.

On this slide
Constraint: A condition a candidate must satisfy, such as MAE at most 3 and latency at most 10 ms.
Latency: Time taken to produce a prediction under stated measurement conditions. Hardware and measurement method matter.

Continue to
Tie-break and Hyperparameter

## Slide 6 — Tie-break and Hyperparameter

Tie-break and Hyperparameter
CML3111, Week 12, slide 6

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
Tie-break: A published rule for choosing between candidates that tie on the main criterion.
Hyperparameter: A setting chosen before fitting, such as tree depth. Tune using validation or cross-validation, not the final test.

Continue to
Error and practical constraints

## Slide 7 — Error and practical constraints

Error and practical constraints
CML3111, Week 12, slide 7

Explanation to give
Separate eligibility from ranking. A model that violates a required error or latency limit cannot win merely because another score is attractive. Latency is time per prediction in the stated measurement setting.

Worked illustration / lecturer answer
With limits MAE <= 5 and latency <= 10 ms, a candidate at MAE 4 and 12 ms fails eligibility. A candidate at MAE 5 and 10 ms passes inclusive limits.

Misconception to address
Establish units and whether boundaries are inclusive. An error of 4 is not comparable across different target units or evaluation samples.

On this slide
A smaller error can require more computation.

A candidate must meet every stated requirement.

Compare eligible models on the same validation observations.

Follow the published tie-break rule when scores tie.

Continue to
A model comparison needs a fair test

## Slide 8 — A model comparison needs a fair test

A model comparison needs a fair test
CML3111, Week 12, slide 8

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Use the same validation observations for every candidate.

Fit preprocessing on training data only.

Choose the error measure and practical requirements before inspecting results.

Continue to
Eligibility comes before ranking

## Slide 9 — Eligibility comes before ranking

Eligibility comes before ranking
CML3111, Week 12, slide 9

Explanation to give
Separate eligibility from ranking. A model that violates a required error or latency limit cannot win merely because another score is attractive. Latency is time per prediction in the stated measurement setting.

Worked illustration / lecturer answer
With limits MAE <= 5 and latency <= 10 ms, a candidate at MAE 4 and 12 ms fails eligibility. A candidate at MAE 5 and 10 ms passes inclusive limits.

Misconception to address
Establish units and whether boundaries are inclusive. An error of 4 is not comparable across different target units or evaluation samples.

On this slide
First check every stated requirement for each candidate.

Reject a candidate that fails even one requirement.

Rank the eligible candidates using the published tie-break rule.

Continue to
A constrained model choice

## Slide 10 — A constrained model choice

A constrained model choice
CML3111, Week 12, slide 10

Explanation to give
Separate eligibility from ranking. A model that violates a required error or latency limit cannot win merely because another score is attractive. Latency is time per prediction in the stated measurement setting.

Worked illustration / lecturer answer
With limits MAE <= 5 and latency <= 10 ms, a candidate at MAE 4 and 12 ms fails eligibility. A candidate at MAE 5 and 10 ms passes inclusive limits.

Misconception to address
Establish units and whether boundaries are inclusive. An error of 4 is not comparable across different target units or evaluation samples.

On this slide
Candidate | Validation error | Time (ms)
simple | 3 | 2
complex | 1 | 20
Invented requirements: error at most 3 and time at most 10 ms.

Continue to
Candidate records and eligibility

## Slide 11 — Candidate records and eligibility

Candidate records and eligibility
CML3111, Week 12, slide 11

Explanation to give
Separate eligibility from ranking. A model that violates a required error or latency limit cannot win merely because another score is attractive. Latency is time per prediction in the stated measurement setting.

Worked illustration / lecturer answer
With limits MAE <= 5 and latency <= 10 ms, a candidate at MAE 4 and 12 ms fails eligibility. A candidate at MAE 5 and 10 ms passes inclusive limits.

Misconception to address
Establish units and whether boundaries are inclusive. An error of 4 is not comparable across different target units or evaluation samples.

On this slide
A candidate is one model under consideration. Its dictionary records a name, a validation error and measured run time.

An eligible candidate meets every published constraint. Build a list of eligible records first. If the list is empty, use the task’s specified no-candidate result.

Continue to
Model selection in Python (1/2)

## Slide 12 — Model selection in Python (1/2)

Model selection in Python (1/2)
CML3111, Week 12, slide 12

Explanation to give
First filter candidates using the published eligibility limits. Rank the survivors with the stated error, speed and tie-break order. If none qualify, return the required no-selection result.

Worked illustration / lecturer answer
A model with lower MAE but excessive prediction time is ineligible when latency is a hard constraint. Test a candidate exactly on each limit to check inclusive comparisons.

Misconception to address
Do not rank before enforcing constraints or silently relax a limit to produce a winner.

Read the displayed code line by line
candidates = [{"name": "simple", "error": 3, "ms": 2},
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

{"name": "complex", "error": 1, "ms": 20}]
This line continues the surrounding expression or block; read it together with the preceding line rather than running it alone.

eligible = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for item in candidates:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

if item["error"] <= 3 and item["ms"] <= 10:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

eligible.append(item)
Evaluate the argument and add it as one new item at the end of this list.

names = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for item in eligible:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

names.append(item["name"])
Evaluate the argument and add it as one new item at the end of this list.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Model selection in Python (2/2)

## Slide 13 — Model selection in Python (2/2)

Model selection in Python (2/2)
CML3111, Week 12, slide 13

Explanation to give
First filter candidates using the published eligibility limits. Rank the survivors with the stated error, speed and tie-break order. If none qualify, return the required no-selection result.

Worked illustration / lecturer answer
A model with lower MAE but excessive prediction time is ineligible when latency is a hard constraint. Test a candidate exactly on each limit to check inclusive comparisons.

Misconception to address
Do not rank before enforcing constraints or silently relax a limit to produce a winner.

Read the displayed code line by line
print(names)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Model selection results

## Slide 14 — Model selection results

Model selection results
CML3111, Week 12, slide 14

Explanation to give
First filter candidates using the published eligibility limits. Rank the survivors with the stated error, speed and tie-break order. If none qualify, return the required no-selection result.

Worked illustration / lecturer answer
A model with lower MAE but excessive prediction time is ineligible when latency is a hard constraint. Test a candidate exactly on each limit to check inclusive comparisons.

Misconception to address
Do not rank before enforcing constraints or silently relax a limit to produce a winner.

On this slide
['simple']

Continue to
A tuple supplies an ordered ranking key

## Slide 15 — A tuple supplies an ordered ranking key

A tuple supplies an ordered ranking key
CML3111, Week 12, slide 15

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
A tuple holds several values in order, such as (error, time, name).

Python compares the first values. A tie moves the comparison to the second.

If those also tie, the third value decides.

Continue to
Trace a tuple ranking key

## Slide 16 — Trace a tuple ranking key

Trace a tuple ranking key
CML3111, Week 12, slide 16

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
Candidate | Key: error, ms, name | Position
beta | (2, 5, "beta") | 1: lower error
alpha | (3, 1, "alpha") | 2: tie on error; faster
gamma | (3, 2, "gamma") | 3: same error; slower
Only eligible candidates reach ranking. If error and time tie, compare the names alphabetically.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Pass a function as the sorting key

## Slide 17 — Pass a function as the sorting key

Pass a function as the sorting key
CML3111, Week 12, slide 17

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
sorted returns a new list in order. In sorted(eligible, key=rank), rank is the function itself, passed without calling it.

sorted calls rank(item) for each candidate and compares the returned tuples. Writing rank() here would call it immediately without its required input.

The original eligible list is unchanged. Check len(ordered) before using ordered[0], because an empty list has no first position.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Sorting with a tie-break rule

## Slide 18 — Sorting with a tie-break rule

Sorting with a tie-break rule
CML3111, Week 12, slide 18

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
A tuple is an ordered group of values.

Python compares the first item, then the second when tied, then the third.

The key function gives sorted the tuple for each candidate.

Guard an empty list before selecting position zero.

Continue to
Sorting with a named function

## Slide 19 — Sorting with a named function

Sorting with a named function
CML3111, Week 12, slide 19

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

On this slide
Expression | Meaning
key=rank | Use rank to build each comparison key
sorted(eligible, key=rank) | Return a newly ordered list
ordered[0] | Select its first item
len(ordered) == 0 | Check for no eligible candidate
Check for an empty list before accessing position zero.

Continue to
Sorting with a tie-break rule in Python

## Slide 20 — Sorting with a tie-break rule in Python

Sorting with a tie-break rule in Python
CML3111, Week 12, slide 20

Explanation to give
A ranking key states the priorities in order. Python compares tuples by the first element, then the second only on a tie, and so on. A key function returns that tuple for one candidate.

Worked illustration / lecturer answer
Keys (3,8,"A") and (3,6,"B") tie on error 3, so latency 6 wins. A third label component makes a remaining exact tie deterministic.

Misconception to address
sorted returns a new ordered list. It does not select only eligible candidates unless filtering happened first. Follow the published priority order.

Read the displayed code line by line
def rank(item):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

return (item["error"], item["ms"], item["name"])
Evaluate this result and send it to the caller, ending this function call.

ordered = sorted(eligible, key=rank)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

if len(ordered) == 0:
Evaluate this yes/no condition. Execute its indented body only on the matching path.

winner = None
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

else:
Use this remaining path when the matching earlier condition did not succeed.

winner = ordered[0]["name"]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(winner)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Local explanation and Conditions of use

## Slide 21 — Local explanation and Conditions of use

Local explanation and Conditions of use
CML3111, Week 12, slide 21

Explanation to give
Connect a model recommendation to the observed evaluation and the intended operating conditions. A local explanation describes one prediction; it does not prove a universal causal rule.

Worked illustration / lecturer answer
A useful statement is “This model met the stated error and latency limits on held-out equipment; validate it on the intended site before operational use.” Point to the comparison table supporting each part.

Misconception to address
Feature importance or one prediction explanation cannot establish that changing the feature would cause the predicted effect.

On this slide
Local explanation: Why a model made one particular prediction. This is different from global importance, which summarises behaviour over many cases.
Conditions of use: The cases and operating circumstances for which the available evidence supports considering the model.

Continue to
A recommendation needs evidence

## Slide 22 — A recommendation needs evidence

A recommendation needs evidence
CML3111, Week 12, slide 22

Explanation to give
Connect a model recommendation to the observed evaluation and the intended operating conditions. A local explanation describes one prediction; it does not prove a universal causal rule.

Worked illustration / lecturer answer
A useful statement is “This model met the stated error and latency limits on held-out equipment; validate it on the intended site before operational use.” Point to the comparison table supporting each part.

Misconception to address
Feature importance or one prediction explanation cannot establish that changing the feature would cause the predicted effect.

On this slide
State the question and the chosen candidate.

Give the evaluation result and the constraint it satisfies.

State a limitation and the evidence that could change the recommendation.

Continue to
Revision example and answer

## Slide 23 — Revision example and answer

Revision example and answer
CML3111, Week 12, slide 23

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: A third model has error 3 and latency 1 ms. Under lowest error then lowest latency, which eligible model wins?

Answer: The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 24 — Preparing for the assignment

Preparing for the assignment
CML3111, Week 12, slide 24

Explanation to give
For W12, read the candidate fields exactly: name, validation_mae and latency_ms. Enforce both inclusive limits before ranking by error, latency and alphabetical name.

Worked illustration / lecturer answer
A candidate exactly at both limits is eligible. If the eligible list is empty, return None. The simpler error/ms names on practice slides must be adapted to the assignment’s published field names.

Misconception to address
A sensible general recommendation does not replace the exact graded return interface. Keep the function contract and the wider project discussion distinct.

On this slide
W12 uses fields name, validation_mae and latency_ms.

Meet both inclusive constraints, then rank by error, latency and alphabetical name.

Return None if no candidate qualifies.

Complete the error function and interpret the separately supplied scenario.

Continue to
Preparing for the assignment continued

## Slide 25 — Preparing for the assignment continued

Preparing for the assignment continued
CML3111, Week 12, slide 25

Explanation to give
For W12, read the candidate fields exactly: name, validation_mae and latency_ms. Enforce both inclusive limits before ranking by error, latency and alphabetical name.

Worked illustration / lecturer answer
A candidate exactly at both limits is eligible. If the eligible list is empty, return None. The simpler error/ms names on practice slides must be adapted to the assignment’s published field names.

Misconception to address
A sensible general recommendation does not replace the exact graded return interface. Keep the function contract and the wider project discussion distinct.

On this slide
Keep project comparisons and graded interfaces distinct.

Continue to
Fair comparison and explanation

## Slide 26 — Fair comparison and explanation

Fair comparison and explanation
CML3111, Week 12, slide 26

Explanation to give
Connect a model recommendation to the observed evaluation and the intended operating conditions. A local explanation describes one prediction; it does not prove a universal causal rule.

Worked illustration / lecturer answer
A useful statement is “This model met the stated error and latency limits on held-out equipment; validate it on the intended site before operational use.” Point to the comparison table supporting each part.

Misconception to address
Feature importance or one prediction explanation cannot establish that changing the feature would cause the predicted effect.

On this slide
Compare the same metric on the same validation cases with the same preprocessing rules.

A small difference needs context, including variation across splits.

Code run out of order can overwrite the variable holding a model; restart and run from the top.

A local explanation addresses one prediction; global importance summarises many.

Continue to
Fair comparison and explanation continued

## Slide 27 — Fair comparison and explanation continued

Fair comparison and explanation continued
CML3111, Week 12, slide 27

Explanation to give
Connect a model recommendation to the observed evaluation and the intended operating conditions. A local explanation describes one prediction; it does not prove a universal causal rule.

Worked illustration / lecturer answer
A useful statement is “This model met the stated error and latency limits on held-out equipment; validate it on the intended site before operational use.” Point to the comparison table supporting each part.

Misconception to address
Feature importance or one prediction explanation cannot establish that changing the feature would cause the predicted effect.

On this slide
A post-hoc explanation of a complex model is not its directly readable internal rule.

Continue to
Your issued task

## Slide 28 — Your issued task

Your issued task
CML3111, Week 12, slide 28

Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate motor winding temperature.

Target units: deg C.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

Continue to
select_model(candidates, max_mae, max_ms)

## Slide 29 — select_model(candidates, max_mae, max_ms)

select_model(candidates, max_mae, max_ms)
CML3111, Week 12, slide 29

Explanation to give
Filter by both published limits, then apply the full tie-break rule. Return the requested model identifier or the specified no-candidate result.

Worked illustration / lecturer answer
Check an exactly-on-limit candidate, a tied pair and an empty eligible list. These are ordinary contract cases rather than optional extensions.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Candidates have name, validation_mae and latency_ms.

Keep those meeting both inclusive constraints; select smallest validation_mae, then latency_ms, then name alphabetically.

Return the selected name or None.

Never use test scores for selection.

Continue to
regression_errors(actual, predicted)

## Slide 30 — regression_errors(actual, predicted)

regression_errors(actual, predicted)
CML3111, Week 12, slide 30

Explanation to give
Pair actual and predicted values by position. Return mae and rmse with full numerical precision.

Worked illustration / lecturer answer
On separate teaching pairs with errors 2 and 4, MAE is 3 and RMSE is sqrt(10). Rounding is for a labelled display, not for the returned metric.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return mae and rmse, calculated over the same paired observations, with full precision.

Continue to
Written evidence

## Slide 31 — Written evidence

Written evidence
CML3111, Week 12, slide 31

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
Model recommendation submission

## Slide 32 — Model recommendation submission

Model recommendation submission
CML3111, Week 12, slide 32

Explanation to give
This slide hands over CML3111 W12. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-27T14:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 27 Nov 2026, 11:00 Kampala

Deadline: 27 Nov 2026, 14:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Project preparation

## Slide 33 — Project preparation

Project preparation
CML3111, Week 12, slide 33

Explanation to give
Make contribution evidence specific enough to check. A seed records the starting state of random choices; a contribution log records who produced and explained which work.

Worked illustration / lecturer answer
Name a file, function or chart and the decision behind it. Match that entry to meaningful repository history. Disclose AI assistance according to the assessment policy.

Misconception to address
Many commits do not necessarily mean substantial work, and a seed does not establish accuracy. Both are supporting evidence, not replacements for the analysis.

On this slide
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 18 Dec 2026, 11:00 Kampala

Continue to
Week 12 quiz

## Slide 34 — Week 12 quiz

Week 12 quiz
CML3111, Week 12, slide 34

Explanation to give
This is the CML3111 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3111 when ready and read the logged closing time.

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

## Slide 35 — Revision and submission checklist

Revision and submission checklist
CML3111, Week 12, slide 35

Explanation to give
A recommendation must satisfy the practical limits before it wins on a ranking metric. Explain eligibility and tie-breaking separately.

Worked illustration / lecturer answer
A model at 4 error units and 12 ms fails a 10 ms limit even if its error is attractive. Test exact boundaries before ranking eligible candidates.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can justify a valid candidate with evidence and a stated limitation.

Save your work and check the required submission files.

Continue to
Optional revision video

## Slide 36 — Optional revision video

Optional revision video
CML3111, Week 12, slide 36

Explanation to give
Give the viewing question before playing the excerpt: Why evaluate using observations not used to fit that particular model?

Worked illustration / lecturer answer
Use the adjacent worked example as the explanation if the video cannot load. Pause after the relevant example and connect its terms to the names and units already used in this lesson. Preview the displayed link and excerpt before class.

Misconception to address
The video is supporting revision, not a replacement for defining the symbols or a requirement to watch a full tutorial during limited class time.

On this slide
For revision after class.

StatQuest with Josh Starmer
Machine Learning Fundamentals Cross Validation

Opening up to 04:00, optional preview-selected excerpt

Listening question: Why evaluate using observations not used to fit that particular model?

Reference / existing resource
https://www.youtube.com/watch?v=fSytzGwwBVw
