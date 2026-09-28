# CML3111 Week11 Engineering

Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.

## Slide 1 — Creating and testing a useful feature

PURPOSE
Creating and testing a useful feature

CONNECT
Previous slide: the preceding week.

EXPLAIN
Communications, Electrical, Mechatronics and Robotics Engineering

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
Previous slide: Creating and testing a useful feature.

EXPLAIN
Create a feature from available measurements.

Compare models with one controlled change.

LECTURER CUE
Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: Five independent features, a full ColumnTransformer construction and domain-code features are extension. Never invent engineering limits.

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
We already keep evaluation data separate. Now we change one input representation while keeping the comparison protocol fixed.

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
A calculated input may help a model. We compare the original and extended inputs on the same observations, then decide whether the evidence supports the extra feature.

LECTURER CUE
A team records device temperature to investigate cooling. Use a communications cabinet, an electrical enclosure or a robot controller as the physical example. No specialist hardware knowledge is assumed.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A feature has a meaning.

REFERENCES


## Slide 5 — A feature has a meaning

PURPOSE
A feature has a meaning

CONNECT
Previous slide: Why this week’s tools are needed.

EXPLAIN
A feature is an input available at prediction time.

An interaction multiplies two inputs to express a joint pattern.

A better validation score can still reflect leakage.

Compare the same observations and explain the physical meaning.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Derived feature and Ratio and interaction.

REFERENCES


## Slide 6 — Derived feature and Ratio and interaction

PURPOSE
Derived feature and Ratio and interaction

CONNECT
Previous slide: A feature has a meaning.

EXPLAIN
Derived feature: A new input calculated from existing inputs. Its definition and unit must be stated.

Ratio and interaction: A ratio divides quantities; an interaction multiplies them. Both need a domain explanation and a unit check.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the physical example across programmes.

REFERENCES


## Slide 7 — Read the physical example across programmes

PURPOSE
Read the physical example across programmes

CONNECT
Previous slide: Derived feature and Ratio and interaction.

EXPLAIN
Current I is the flow of electric charge, measured in amperes (A). Resistance R opposes that flow, measured in ohms.

Power P is energy transferred per second, measured in watts (W). Resistive heating follows P = I²R in this example.

I² means I × I. With I = 2 A and R = 3 ohms, P = 2 × 2 × 3 = 12 W. This relationship motivates a feature; evaluation still tests whether it helps.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A physical relationship can form a feature.

REFERENCES


## Slide 8 — A physical relationship can form a feature

PURPOSE
A physical relationship can form a feature

CONNECT
Previous slide: Read the physical example across programmes.

EXPLAIN
Explain each quantity and the unit of the result.

LECTURER CUE
Ask students to describe what they see before introducing terminology. Generated conceptual teaching illustration.  Source: figs/experiential/ASSET_SOURCES.md.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
An interaction uses two known inputs.

REFERENCES


## Slide 9 — An interaction uses two known inputs

PURPOSE
An interaction uses two known inputs

CONNECT
Previous slide: A physical relationship can form a feature.

EXPLAIN
Current A | Resistance ohm | I squared × R W

2 | 3 | 12

4 | 3 | 48

A derived input must be available when predicting. A useful physical relationship still needs validation.

LECTURER CUE
A derived input must be available when predicting. A useful physical relationship still needs validation.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A percentage and its fraction.

REFERENCES


## Slide 10 — A percentage and its fraction

PURPOSE
A percentage and its fraction

CONNECT
Previous slide: An interaction uses two known inputs.

EXPLAIN
40% means 40 out of 100.

40 / 100 gives 0.4.

This changes the representation. It adds no new observation.

LECTURER CUE
Begin with a percentage: 40% means 40 / 100 = 0.4. Converting percentage to fraction changes units but adds no new information.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
A combined input needs a reason.

REFERENCES


## Slide 11 — A combined input needs a reason

PURPOSE
A combined input needs a reason

CONNECT
Previous slide: A percentage and its fraction.

EXPLAIN
An interaction multiplies two inputs.

It may help a simple model represent a joint pattern.

An interaction with degrees Celsius is an empirical feature, not automatically a physical law.

LECTURER CUE
An interaction may help a simple model express a relationship, but usefulness is tested rather than assumed. An interaction involving Celsius is an empirical feature, not automatically a physical law.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Ablation and Improvement.

REFERENCES


## Slide 12 — Ablation and Improvement

PURPOSE
Ablation and Improvement

CONNECT
Previous slide: A combined input needs a reason.

EXPLAIN
Ablation: Compare a model with and without a feature while keeping the data partitions, model family and metric fixed.

Improvement: For an error metric, baseline error minus new error. A negative result means the added feature worsened validation error in that comparison.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
One change makes a comparison interpretable.

REFERENCES


## Slide 13 — One change makes a comparison interpretable

PURPOSE
One change makes a comparison interpretable

CONNECT
Previous slide: Ablation and Improvement.

EXPLAIN
Base MAE is 3.0. Extended MAE is 2.5.

Improvement = base error minus extended error = 0.5.

Keep the training rows, validation rows, model family and metric fixed.

LECTURER CUE
Read a two-row results table: base MAE 3, extended MAE 2.5 gives improvement 0.5 target units. Ask which other experimental choices must stay fixed.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Worked example.

REFERENCES


## Slide 14 — Feature comparisons in Python

PURPOSE
Feature comparisons in Python

CONNECT
Previous slide: One change makes a comparison interpretable.

EXPLAIN
Read the code in this order:
load_pct = 40
ambient_c = 25
load_fraction = load_pct / 100
interaction = load_pct * ambient_c
print(load_fraction, interaction)
base_mae = 3.0
extended_mae = 2.5
print(base_mae - extended_mae)

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Begin with a percentage: 40% means 40 / 100 = 0.4. Converting percentage to fraction changes units but adds no new information. An interaction may help a simple model express a relationship, but usefulness is tested rather than assumed. An interaction involving Celsius is an empirical feature, not automatically a physical law. Read a two-row results table: base MAE 3, extended MAE 2.5 gives improvement 0.5 target units. Ask which other experimental choices must stay fixed.

Complete practice code:
load_pct = 40
ambient_c = 25
load_fraction = load_pct / 100
interaction = load_pct * ambient_c
print(load_fraction, interaction)
base_mae = 3.0
extended_mae = 2.5
print(base_mae - extended_mae)

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Expected output.

REFERENCES


## Slide 15 — Feature comparisons results

PURPOSE
Feature comparisons results

CONNECT
Previous slide: Feature comparisons in Python.

EXPLAIN
0.4 1000
0.5

LECTURER CUE
Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Read the two-model experiment.

REFERENCES


## Slide 16 — Read the two-model experiment

PURPOSE
Read the two-model experiment

CONNECT
Previous slide: Feature comparisons results.

EXPLAIN
Each row contains a pair of inputs. for a, b in rows assigns the first entry to a and the second to b, then repeats the block.

with_interaction returns a new table containing a, b and a × b. Both models keep the same training and validation rows.

Create the model first, then call fit on the next line. round(value, 6) rounds a displayed number to six decimal places; retain full precision for calculations.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Trace the interaction-building function.

REFERENCES


## Slide 17 — Trace the interaction-building function

PURPOSE
Trace the interaction-building function

CONNECT
Previous slide: Read the two-model experiment.

EXPLAIN
Each row contains two inputs. for a, b in rows: assigns them to a and b. [a, b, a * b] builds a new row with their product as a third input.

For row [2, 3], append [2, 3, 6]. For row [4, 5], append [4, 5, 20]. The function returns the newly built list of rows.

The same function must transform both training and validation inputs. It uses no target values to construct the new feature.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two models under one protocol.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 18 — Two models under one protocol

PURPOSE
Two models under one protocol

CONNECT
Previous slide: Trace the interaction-building function.

EXPLAIN
Run this complete practice experiment in a fresh session.

Both models use the same rows and targets; the second receives one additional input.

Read every column before fitting.

This invented experiment illustrates procedure, not a measured engineering benefit.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two models under one protocol in Python (1/3).

REFERENCES


## Slide 19 — Two models under one protocol in Python (1/3)

PURPOSE
Two models under one protocol in Python (1/3)

CONNECT
Previous slide: Two models under one protocol.

EXPLAIN
Read the code in this order:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]

import loads a library. from selects a tool from it.

Square brackets create a list or select an item.

= assigns the value on the right to the name on the left.

Read top to bottom. Run the complete example in the matching practice notebook.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two models under one protocol in Python (2/3).

REFERENCES


## Slide 20 — Two models under one protocol in Python (2/3)

PURPOSE
Two models under one protocol in Python (2/3)

CONNECT
Previous slide: Two models under one protocol in Python (1/3).

EXPLAIN
Read the code in this order:
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression()
base.fit(train, y)
extended = LinearRegression()
extended.fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)

def names the function. Inputs go inside parentheses.

for takes the next item. The indented block repeats.

return sends the result back to the caller.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Two models under one protocol in Python (3/3).

REFERENCES


## Slide 21 — Two models under one protocol in Python (3/3)

PURPOSE
Two models under one protocol in Python (3/3)

CONNECT
Previous slide: Two models under one protocol in Python (2/3).

EXPLAIN
Read the code in this order:
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

predict applies the fitted model to new inputs.

print displays a value below the cell.

= assigns the value on the right to the name on the left.

Continue the SAME cell; keep indentation. Run after all parts are entered.

LECTURER CUE
Run this complete practice experiment in a fresh session. Both models use the same rows and targets; the second receives one additional input. Read every column before fitting. This invented experiment illustrates procedure, not a measured engineering benefit.

Complete practice code:
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
train = [[1, 2], [2, 3], [3, 2], [4, 4], [5, 3]]
y = [3, 5, 5, 8, 8]
validation = [[2, 2], [3, 3]]
truth = [4, 6]
def with_interaction(rows):
    result = []
    for a, b in rows:
        result.append([a, b, a * b])
    return result
base = LinearRegression().fit(train, y)
extended = LinearRegression().fit(with_interaction(train), y)
base_predictions = base.predict(validation)
base_error = mean_absolute_error(truth, base_predictions)
print(round(base_error, 6))
validation_features = with_interaction(validation)
extended_predictions = extended.predict(validation_features)
error = mean_absolute_error(truth, extended_predictions)
print(round(error, 6))

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Scaling changes units of comparison.

REFERENCES


## Slide 22 — Scaling changes units of comparison

PURPOSE
Scaling changes units of comparison

CONNECT
Previous slide: Two models under one protocol in Python (3/3).

EXPLAIN
A distance calculation can be dominated by a feature with larger numerical values. Scaling puts feature values on a chosen numerical scale.

One example is (value - training_min) / (training_max - training_min). With training limits 10 and 30, value 20 becomes 10 / 20 = 0.5.

Use the same learned limits for new observations. A zero training range needs a defined handling rule. New values outside the training range may scale outside 0 to 1.



Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Encoding and Scaling.

REFERENCES
Reference: https://docs.python.org/3/tutorial/introduction.html and https://docs.python.org/3/tutorial/controlflow.html; original teaching examples.

## Slide 23 — Encoding and Scaling

PURPOSE
Encoding and Scaling

CONNECT
Previous slide: Scaling changes units of comparison.

EXPLAIN
Encoding: Representing a category numerically. One-hot uses separate indicator columns. Arbitrary integer labels can falsely suggest an order.

Scaling: Changing the numerical scale of features. Fit learned scaling on training data only. It matters for distance-based models but is not required by ordinary decision trees.

LECTURER CUE
Explain the definitions before running or tracing the example. Point to the line or table row that produces each result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Revision example and answer.

REFERENCES


## Slide 24 — Revision example and answer

PURPOSE
Revision example and answer

CONNECT
Previous slide: Encoding and Scaling.

EXPLAIN
Example: If the extended error becomes 3.4, calculate improvement and decide whether this evidence supports retaining the feature.

Answer: Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.

LECTURER CUE
Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Preparing for the assignment.

REFERENCES


## Slide 25 — Preparing for the assignment

PURPOSE
Preparing for the assignment

CONNECT
Previous slide: Revision example and answer.

EXPLAIN
W11 names four output features and a two-model ablation.

Explain output order, preservation of input rows, full precision and training-only fitting.

Use the supplied written scenario for the interpretation requested there.

Do not substitute this practice example’s result.

LECTURER CUE
W11 names four output features and a two-model ablation. Explain output order, preservation of input rows, full precision and training-only fitting. Use the supplied written scenario for the interpretation requested there. Do not substitute this practice example’s result.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Features without misleading evaluation.

REFERENCES


## Slide 26 — Features without misleading evaluation

PURPOSE
Features without misleading evaluation

CONNECT
Previous slide: Preparing for the assignment.

EXPLAIN
Rescaling an input usually does not change the partitions available to an ordinary decision tree.

An identifier or a future-known field can create an apparent improvement without useful predictive information.

Dividing by zero can produce infinity or an error; decide what the denominator means before replacing it.

LECTURER CUE
Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Features without misleading evaluation continued.

REFERENCES


## Slide 27 — Features without misleading evaluation continued

PURPOSE
Features without misleading evaluation continued

CONNECT
Previous slide: Features without misleading evaluation.

EXPLAIN
Read ablation differences using the same error definition, and explain features using domain knowledge.

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
Previous slide: Features without misleading evaluation continued.

EXPLAIN
Investigate motor winding temperature.

Target units: deg C.

These are synthetic teaching records, not measurements suitable for deployment.

Each record is one operating observation; equipment_id repeats across observations.

LECTURER CUE
Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
make_features(feature_records).

REFERENCES


## Slide 29 — make_features(feature_records)

PURPOSE
make_features(feature_records)

CONNECT
Previous slide: Your issued task.

EXPLAIN
Return one feature row per input, in order: [load_pct, ambient_c, load_pct/100, load_pct*ambient_c].

Use inputs available at prediction time only.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W11/CML3111/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
ablation_metrics(training_records, validation_records).

REFERENCES


## Slide 30 — ablation_metrics(training_records, validation_records)

PURPOSE
ablation_metrics(training_records, validation_records)

CONNECT
Previous slide: make_features(feature_records).

EXPLAIN
Fit two sklearn LinearRegression models on the same training records: base features [load_pct, ambient_c] and extended features adding load_pct*ambient_c.

Evaluate both on the same validation records.

Return base_mae, extended_mae and improvement=base_mae-extended_mae, without rounding.

Inputs are complete; never fit on validation targets.

LECTURER CUE
Public task contract. Explain input and output types before independent work. Source: IUEA_Teaching_Plan/assessment_banks/W11/CML3111/A/TASKS.md

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Written evidence.

REFERENCES


## Slide 31 — Written evidence

PURPOSE
Written evidence

CONNECT
Previous slide: ablation_metrics(training_records, validation_records).

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
Features and ablation submission.

REFERENCES


## Slide 32 — Features and ablation submission

PURPOSE
Features and ablation submission

CONNECT
Previous slide: Written evidence.

EXPLAIN
Opens: 20 Nov 2026, 11:00 Kampala

Deadline: 27 Nov 2026, 11:00 Kampala

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
Previous slide: Features and ablation submission.

EXPLAIN
Use the published machine learning project brief.

Build the evidence gradually in your project notebook.

Keep raw data, labelled charts, run instructions and individual contributions.

Published deadline: 18 Dec 2026, 11:00 Kampala

LECTURER CUE
Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Week 11 quiz.

REFERENCES


## Slide 34 — Week 11 quiz

PURPOSE
Week 11 quiz

CONNECT
Previous slide: Project preparation.

EXPLAIN
Answer individually after the lecturer activates the quiz.

Available for 24 hours from activation.

Use your Student Registration Number and registered account.

The lecturer will confirm the exact closing time.

LECTURER CUE
Activate the matching open_W11_CML3111 function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
Before you leave.

REFERENCES


## Slide 35 — Revision and submission checklist

PURPOSE
Revision and submission checklist

CONNECT
Previous slide: Week 11 quiz.

EXPLAIN
You can state the new feature’s meaning and calculate an improvement correctly.

Save your work and check the required submission files.

LECTURER CUE
Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.

TEACHING MODE
Demonstrate first. Read each new symbol aloud, trace the values and compare the shown output. Learners repeat worked examples individually after class.

NEXT
independent revision and the issued task.

REFERENCES
