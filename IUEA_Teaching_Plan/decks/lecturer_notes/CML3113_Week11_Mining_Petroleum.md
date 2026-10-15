# CML3113 Week11 Mining Petroleum

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Creating and testing a useful feature

Creating and testing a useful feature
CML3113, Week 11, slide 1

Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Mining and Petroleum Engineering

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3113, Week 11, slide 2

Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Create a feature from available measurements.

Compare models with one controlled change.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3113, Week 11, slide 3

Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
We already keep evaluation data separate. Now we change one input representation while keeping the comparison protocol fixed.

Continue to
Why this week’s tools are needed

## Slide 4 — Why this week’s tools are needed

Why this week’s tools are needed
CML3113, Week 11, slide 4

Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
A calculated input may help a model. We compare the original and extended inputs on the same observations, then decide whether the evidence supports the extra feature.

Continue to
A feature has a meaning

## Slide 5 — A feature has a meaning

A feature has a meaning
CML3113, Week 11, slide 5

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
A feature is an input available at prediction time.

An interaction multiplies two inputs to express a joint pattern.

A better validation score can still reflect leakage.

Compare the same observations and explain the physical meaning.

Continue to
Derived feature and Ratio and interaction

## Slide 6 — Derived feature and Ratio and interaction

Derived feature and Ratio and interaction
CML3113, Week 11, slide 6

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Derived feature: A new input calculated from existing inputs. Its definition and unit must be stated.
Ratio and interaction: A ratio divides quantities; an interaction multiplies them. Both need a domain explanation and a unit check.

Continue to
Read the physical example across programmes

## Slide 7 — Read the physical example across programmes

Read the physical example across programmes
CML3113, Week 11, slide 7

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Current I is the flow of electric charge, measured in amperes (A). Resistance R opposes that flow, measured in ohms.

Power P is energy transferred per second, measured in watts (W). Resistive heating follows P = I²R in this example.

I² means I × I. With I = 2 A and R = 3 ohms, P = 2 × 2 × 3 = 12 W. This relationship motivates a feature; evaluation still tests whether it helps.

Continue to
A physical relationship can form a feature

## Slide 8 — A physical relationship can form a feature

A physical relationship can form a feature
CML3113, Week 11, slide 8

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Explain each quantity and the unit of the result.

Continue to
An interaction uses two known inputs

## Slide 9 — An interaction uses two known inputs

An interaction uses two known inputs
CML3113, Week 11, slide 9

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Current A | Resistance ohm | I squared × R W
2 | 3 | 12
4 | 3 | 48
A derived input must be available when predicting. A useful physical relationship still needs validation.

Continue to
A percentage and its fraction

## Slide 10 — A percentage and its fraction

A percentage and its fraction
CML3113, Week 11, slide 10

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
40% means 40 out of 100.

40 / 100 gives 0.4.

This changes the representation. It adds no new observation.

Continue to
A combined input needs a reason

## Slide 11 — A combined input needs a reason

A combined input needs a reason
CML3113, Week 11, slide 11

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
An interaction multiplies two inputs.

It may help a simple model represent a joint pattern.

An interaction with degrees Celsius is an empirical feature, not automatically a physical law.

Continue to
Ablation and Improvement

## Slide 12 — Ablation and Improvement

Ablation and Improvement
CML3113, Week 11, slide 12

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Ablation: Compare a model with and without a feature while keeping the data partitions, model family and metric fixed.
Improvement: For an error metric, baseline error minus new error. A negative result means the added feature worsened validation error in that comparison.

Continue to
One change makes a comparison interpretable

## Slide 13 — One change makes a comparison interpretable

One change makes a comparison interpretable
CML3113, Week 11, slide 13

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Base MAE is 3.0. Extended MAE is 2.5.

Improvement = base error minus extended error = 0.5.

Keep the training rows, validation rows, model family and metric fixed.

Continue to
Feature comparisons in Python

## Slide 14 — Feature comparisons in Python

Feature comparisons in Python
CML3113, Week 11, slide 14

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

Read the displayed code line by line
load_pct = 40
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

ambient_c = 25
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

load_fraction = load_pct / 100
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

interaction = load_pct * ambient_c
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(load_fraction, interaction)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

base_mae = 3.0
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

extended_mae = 2.5
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(base_mae - extended_mae)
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Feature comparisons results

## Slide 15 — Feature comparisons results

Feature comparisons results
CML3113, Week 11, slide 15

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
0.4 1000
0.5

Continue to
Read the two-model experiment

## Slide 16 — Read the two-model experiment

Read the two-model experiment
CML3113, Week 11, slide 16

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Each row contains a pair of inputs. for a, b in rows assigns the first entry to a and the second to b, then repeats the block.

with_interaction returns a new table containing a, b and a × b. Both models keep the same training and validation rows.

Create the model first, then call fit on the next line. round(value, 6) rounds a displayed number to six decimal places; retain full precision for calculations.

Continue to
Trace the interaction-building function

## Slide 17 — Trace the interaction-building function

Trace the interaction-building function
CML3113, Week 11, slide 17

Explanation to give
A derived feature is a new input calculated from known inputs. Explain its physical or operational reason and its units before presenting it to a model. An interaction allows one input's effect to depend on another.

Worked illustration / lecturer answer
For load_pct 50 and ambient_c 30, the course interaction load_pct * ambient_c is 1500. Separately, load_pct / 100 gives the fraction 0.5. These are different derived quantities. The interaction is a hypothesis to test, not a measured law.

Misconception to address
A plausible physical story does not guarantee an improvement. Do not use the target or information that would only become available after the prediction.

On this slide
Each row contains two inputs. for a, b in rows: assigns them to a and b. [a, b, a * b] builds a new row with their product as a third input.

For row [2, 3], append [2, 3, 6]. For row [4, 5], append [4, 5, 20]. The function returns the newly built list of rows.

The same function must transform both training and validation inputs. It uses no target values to construct the new feature.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Two models under one protocol

## Slide 18 — Two models under one protocol

Two models under one protocol
CML3113, Week 11, slide 18

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Run this complete practice experiment in a fresh session.

Both models use the same rows and targets; the second receives one additional input.

Read every column before fitting.

This invented experiment illustrates procedure, not a measured engineering benefit.

Continue to
Two models under one protocol in Python (1/3)

## Slide 19 — Two models under one protocol in Python (1/3)

Two models under one protocol in Python (1/3)
CML3113, Week 11, slide 19

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

Read the displayed code line by line
from sklearn.linear_model import LinearRegression
Bring the named tool from this library into the current Python session.

from sklearn.metrics import mean_absolute_error
Bring the named tool from this library into the current Python session.

train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

y = [3, 5, 5, 8, 8]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

validation = [[2, 2], [3, 3]]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

truth = [4, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Two models under one protocol in Python (2/3)

## Slide 20 — Two models under one protocol in Python (2/3)

Two models under one protocol in Python (2/3)
CML3113, Week 11, slide 20

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

Read the displayed code line by line
def with_interaction(rows):
Store these instructions under this function name. Names in parentheses are its inputs; the body waits until a call.

result = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for a, b in rows:
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

result.append([a, b, a * b])
Evaluate the argument and add it as one new item at the end of this list.

return result
Evaluate this result and send it to the caller, ending this function call.

base = LinearRegression()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

base.fit(train, y)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

extended = LinearRegression()
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

extended.fit(with_interaction(train), y)
Learn from the supplied training rows and their aligned targets. This changes the fitted object’s state.

base_predictions = base.predict(validation)
Apply the already fitted rule to these input rows without passing their true targets.

base_error = mean_absolute_error(truth, base_predictions)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Two models under one protocol in Python (3/3)

## Slide 21 — Two models under one protocol in Python (3/3)

Two models under one protocol in Python (3/3)
CML3113, Week 11, slide 21

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

Read the displayed code line by line
print(round(base_error, 6))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

validation_features = with_interaction(validation)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

extended_predictions = extended.predict(validation_features)
Apply the already fitted rule to these input rows without passing their true targets.

error = mean_absolute_error(truth, extended_predictions)
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

print(round(error, 6))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Continue the SAME cell; keep indentation. Run after all parts are entered.

Continue to
Scaling changes units of comparison

## Slide 22 — Scaling changes units of comparison

Scaling changes units of comparison
CML3113, Week 11, slide 22

Explanation to give
Scaling changes numerical ranges to make inputs comparable for algorithms that are sensitive to magnitude. Learn the scaling values from the training subset and apply the same transformation later.

Worked illustration / lecturer answer
Converting a length from metres to millimetres multiplies its numeric value by 1000 without changing the physical length. Standardisation uses training mean and standard deviation to express relative position.

Misconception to address
Scaling is not evidence that all features are equally useful. Never learn the scaler separately on validation or test observations.

On this slide
A distance calculation can be dominated by a feature with larger numerical values. Scaling puts feature values on a chosen numerical scale.

One example is (value - training_min) / (training_max - training_min). With training limits 10 and 30, value 20 becomes 10 / 20 = 0.5.

Use the same learned limits for new observations. A zero training range needs a defined handling rule. New values outside the training range may scale outside 0 to 1.

Reference / existing resource
https://docs.python.org/3/tutorial/introduction.html
https://docs.python.org/3/tutorial/controlflow.html;

Continue to
Encoding and Scaling

## Slide 23 — Encoding and Scaling

Encoding and Scaling
CML3113, Week 11, slide 23

Explanation to give
One-hot encoding gives each category its own indicator column. A row has a 1 in the column matching its category and 0 in the others.

Worked illustration / lecturer answer
For categories A and B, an A row becomes [1,0] and a B row becomes [0,1]. Assigning A=1 and B=2 could accidentally suggest a meaningful numerical distance or order.

Misconception to address
Fit the encoder on training data and define how to handle categories not seen during training. Do not invent an ordinal meaning for names.

On this slide
Encoding: Representing a category numerically. One-hot uses separate indicator columns. Arbitrary integer labels can falsely suggest an order.
Scaling: Changing the numerical scale of features. Fit learned scaling on training data only. It matters for distance-based models but is not required by ordinary decision trees.

Continue to
Revision example and answer

## Slide 24 — Revision example and answer

Revision example and answer
CML3113, Week 11, slide 24

Explanation to give
Use the displayed example as a short individual revision question, then explain the reasoning behind its answer.

Worked illustration / lecturer answer
Example: If the extended error becomes 3.4, calculate improvement and decide whether this evidence supports retaining the feature.

Answer: Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.

Misconception to address
Trace the operation that changes the value rather than accepting a memorised output. For notebook-state examples, specify which cell is repeated and whether the initialisation ran again.

Continue to
Preparing for the assignment

## Slide 25 — Preparing for the assignment

Preparing for the assignment
CML3113, Week 11, slide 25

Explanation to give
Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.

Worked illustration / lecturer answer
MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.

Misconception to address
Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.

On this slide
W11 names four output features and a two-model ablation.

Keep the original row order and full precision. Fit preprocessing on the training rows only.

Use the supplied written scenario for the interpretation requested there.

Do not substitute this practice example’s result.

Continue to
Features without misleading evaluation

## Slide 26 — Features without misleading evaluation

Features without misleading evaluation
CML3113, Week 11, slide 26

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Rescaling an input usually does not change the partitions available to an ordinary decision tree.

An identifier or a future-known field can create an apparent improvement without useful predictive information.

Dividing by zero can produce infinity or an error; decide what the denominator means before replacing it.

Continue to
Features without misleading evaluation continued

## Slide 27 — Features without misleading evaluation continued

Features without misleading evaluation continued
CML3113, Week 11, slide 27

Explanation to give
An ablation comparison changes one feature or component while holding the evaluation protocol fixed. This helps attribute any observed difference to the change being tested.

Worked illustration / lecturer answer
If validation MAE drops from 5 to 4, the absolute reduction is 1 in the target unit and the relative reduction is 20%. If it rises, the extra feature has not helped under this protocol.

Misconception to address
Changing the split, model and feature at once makes attribution unclear. Use the same observations, metric and fitting rules for both variants.

On this slide
Read ablation differences using the same error definition, and explain features using domain knowledge.

Continue to
Your issued task

## Slide 28 — Your issued task

Your issued task
CML3113, Week 11, slide 28

Explanation to give
Name this cohort’s target and its unit exactly as displayed. Each row is one operating observation, while equipment_id can repeat across several observations.

Worked illustration / lecturer answer
Explain record_id as the identifier of an observation, load_pct as load expressed in percent and ambient_c as temperature in degrees Celsius. The target records the known answer in training data.

Misconception to address
These are synthetic examples for learning. They do not establish a calibrated physical relationship or justify operation of real equipment.

On this slide
Investigate crusher energy demand.

Target units: kWh/t.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

Continue to
make_features(feature_records)

## Slide 29 — make_features(feature_records)

make_features(feature_records)
CML3113, Week 11, slide 29

Explanation to give
Create the requested numeric feature rows in the same order as the input records. Use only information available at prediction time.

Worked illustration / lecturer answer
Distinguish load_pct from load_pct/100. The task’s named interaction uses its exact published formula; a mathematically related alternative would still violate the interface.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c].

Use inputs available at prediction time only.

Continue to
ablation_metrics(training_records, validation_records)

## Slide 30 — ablation_metrics(training_records, validation_records)

ablation_metrics(training_records, validation_records)
CML3113, Week 11, slide 30

Explanation to give
Compare the original and extended feature sets with the same training and validation observations and the same model protocol.

Worked illustration / lecturer answer
Return the specified metrics and improvement calculation. A reduction from MAE 5 to 4 is improvement 1, not -1, when the contract defines before minus after.

Misconception to address
Keep the exact output names and required types. Use the task text for the learner’s own assessed answer; the alternate example explains the method without replacing their work.

On this slide
Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c.

Evaluate both on the same validation records.

Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding.

Inputs are complete; never fit on validation targets.

Continue to
Written evidence

## Slide 31 — Written evidence

Written evidence
CML3113, Week 11, slide 31

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
Features and ablation submission

## Slide 32 — Features and ablation submission

Features and ablation submission
CML3113, Week 11, slide 32

Explanation to give
This slide hands over CML3113 W11. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
The recorded cutoff for this form is 2026-11-27T08:00:00+03:00. Check the live form for later changes. A replacement must contain the complete required file set, not just the changed file.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Opens: 20 Nov 2026, 08:00 Kampala

Deadline: 27 Nov 2026, 08:00 Kampala

Use your full Student Registration Number in the form.

Keep the submitted files and confirmation.

Continue to
Project preparation

## Slide 33 — Project preparation

Project preparation
CML3113, Week 11, slide 33

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

Published deadline: 18 Dec 2026, 08:00 Kampala

Continue to
Week 11 quiz

## Slide 34 — Week 11 quiz

Week 11 quiz
CML3113, Week 11, slide 34

Explanation to give
This is the CML3113 Week 1 quiz. The student link opens the response form; it does not activate its window. In Quiz Controls use open_W1_CML3113 when ready and read the logged closing time.

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
CML3113, Week 11, slide 35

Explanation to give
Explain why a calculated input may help and test the idea under an unchanged validation protocol.

Worked illustration / lecturer answer
If validation MAE falls from 5 to 4 after adding one feature, the reduction is 1 target unit, or 20%. A comparison on a different split cannot isolate that change.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can state the new feature’s meaning and calculate an improvement correctly.

Save your work and check the required submission files.
