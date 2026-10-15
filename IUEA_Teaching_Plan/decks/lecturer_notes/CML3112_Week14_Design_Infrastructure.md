# CML3112 Week14 Design Infrastructure

Lecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.

## Slide 1 — Preparing for Practical Test 2

Preparing for Practical Test 2
CML3112, Week 14, slide 1

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
Use this as an orientation to the lesson. Terms and syntax will be unpacked on their own slides; students do not need to know them in advance.

On this slide
Civil Engineering and Architecture

Continue to
Today’s learning

## Slide 2 — Today’s learning

Today’s learning
CML3112, Week 14, slide 2

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
At the end, check the specific outcome shown here using a small previously demonstrated example. A completed file without an explanation is not evidence of understanding.

On this slide
Rehearse previously taught modelling decisions.

Practise saving the complete test notebook offline.

Continue to
Connection to the previous lesson

## Slide 3 — Connection to the previous lesson

Connection to the previous lesson
CML3112, Week 14, slide 3

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
Connect this to the previous result named on this slide. Demonstrate the first step again if necessary; there is no requirement for partner work before the explanation.

On this slide
Can you name the target, fit only on training records and explain how you would keep the test untouched?

Continue to
Preparation happens before the test

## Slide 4 — Preparation happens before the test

Preparation happens before the test
CML3112, Week 14, slide 4

Explanation to give
Show the offline save location and reopen the file before test day. Identify both the code cells and the markdown cell headed My written evidence.

Worked illustration / lecturer answer
Use a separate practice notebook for rehearsal. Students should locate the actual .ipynb on disk rather than rely on a browser tab or cloud link.

Misconception to address
During the assessed period, report technical failures immediately and follow the invigilator’s instructions. Do not introduce new modelling code or online resources.

On this slide
Practise the already taught error calculations and data-splitting rules.

Use separate practice values.

The timed session follows the issued test instructions.

Continue to
Rehearse the offline save procedure

## Slide 5 — Rehearse the offline save procedure

Rehearse the offline save procedure
CML3112, Week 14, slide 5

Explanation to give
Show the offline save location and reopen the file before test day. Identify both the code cells and the markdown cell headed My written evidence.

Worked illustration / lecturer answer
Use a separate practice notebook for rehearsal. Students should locate the actual .ipynb on disk rather than rely on a browser tab or cloud link.

Misconception to address
During the assessed period, report technical failures immediately and follow the invigilator’s instructions. Do not introduce new modelling code or online resources.

On this slide
Save your notebook on the prepared lab computer.

Type Part B under My written evidence in the notebook.

Locate and reopen the complete notebook without internet.

Continue to
A result needs an explanation

## Slide 6 — A result needs an explanation

A result needs an explanation
CML3112, Week 14, slide 6

Explanation to give
Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.

Worked illustration / lecturer answer
MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.

Misconception to address
Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.

On this slide
Name the target and its unit or class.

Explain which data fitted preprocessing and which data evaluated the model.

A high score alone does not establish a useful engineering model.

Continue to
Practice before test day

## Slide 7 — Practice before test day

Practice before test day
CML3112, Week 14, slide 7

Explanation to give
Pair the actual and predicted values in order. The first absolute error is abs(4-5)=1; the second is abs(8-6)=2.

Worked illustration / lecturer answer
Their mean is (1+2)/2=1.5. The unit is the target unit. Both observations contribute once to the numerator and denominator.

Misconception to address
Use the practice values only before the assessed session. MAE 1.5 is an average, not a maximum error guarantee.

Read the displayed code line by line
actual = [4, 8]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

predicted = [5, 6]
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

errors = []
Evaluate the complete right-hand expression first, then assign its result to the name or selected field on the left.

for a, p in zip(actual, predicted):
Take each item or pair in turn, assign the loop name(s), and repeat the indented body.

errors.append(abs(a - p))
Evaluate the argument and add it as one new item at the end of this list.

print(sum(errors) / len(errors))
Evaluate the expression inside the parentheses and display it. Displaying is separate from returning a function result.

Result / continuity
Read top to bottom. Run the complete example in the matching practice notebook.

Continue to
Test session

## Slide 8 — Test session

Test session
CML3112, Week 14, slide 8

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
At the Part A boundary, follow the official snapshot procedure. During the 25-minute Part B period, students type reasoning but must not execute code. Do not change the published timing during an explanation.

On this slide
00–15 minutes: briefing and file check.

15–135 minutes: individual practical work.

135–160 minutes: typed offline reasoning, with code execution prohibited.

160–180 minutes: save and hand in through invigilated offline collection.

Continue to
Preparation checkpoint

## Slide 9 — Preparation checkpoint

Preparation checkpoint
CML3112, Week 14, slide 9

Explanation to give
Show the offline save location and reopen the file before test day. Identify both the code cells and the markdown cell headed My written evidence.

Worked illustration / lecturer answer
Use a separate practice notebook for rehearsal. Students should locate the actual .ipynb on disk rather than rely on a browser tab or cloud link.

Misconception to address
During the assessed period, report technical failures immediately and follow the invigilator’s instructions. Do not introduce new modelling code or online resources.

On this slide
Each learner can save and reopen the complete notebook in the offline setting.

Continue to
Your evidence

## Slide 10 — Your evidence

Your evidence
CML3112, Week 14, slide 10

Explanation to give
Show the offline save location and reopen the file before test day. Identify both the code cells and the markdown cell headed My written evidence.

Worked illustration / lecturer answer
Use a separate practice notebook for rehearsal. Students should locate the actual .ipynb on disk rather than rely on a browser tab or cloud link.

Misconception to address
During the assessed period, report technical failures immediately and follow the invigilator’s instructions. Do not introduce new modelling code or online resources.

On this slide
Use TEST2’s official brief, interfaces, time allocation, permitted resources and packet requirements.

Follow the test instructions issued by your lecturer.

Continue to
Practical Test 2

## Slide 11 — Practical Test 2

Practical Test 2
CML3112, Week 14, slide 11

Explanation to give
Show the actual markdown answer cell headed My written evidence. This is where the learner explains the choices and the supplied scenario in their own words.

Worked illustration / lecturer answer
A useful explanation connects a decision to a named result and its limitation: for example, why a training-only median avoids using evaluation information. Describe supplied scenario figures as supplied, not as measurements the learner produced.

Misconception to address
Prompts and copied code comments do not substitute for the learner’s reasoning. Weekly work and tests use the notebook; projects also require their separate readable report.

On this slide
Write your own explanation in the markdown cell headed `## My written evidence`.

Keep that heading.

Task prompts and code comments are excluded from reasoning marks.

Complete every original rubric criterion below, not just the checked functions.

Continue to
Practical Test 2 continued

## Slide 12 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 12

Explanation to give
A chart must answer a stated question and show the actual data result. Explain what one mark represents and label both the quantity and unit before stating the finding.

Worked illustration / lecturer answer
A useful caption names the group or sample, the observed difference and the relevant unit. A limitation states what the plotted observations cannot establish, such as causation or performance at a new site.

Misconception to address
Text claiming “a chart was made” is not the required chart. Check the exact number and kinds required on this slide and in the assessment guide.

On this slide
Include profiling, justified cleaning, question-led charts and your engineering recommendation where required.

Keep raw data.

State units and distinguish correlation from causation.

Charts must be actual labelled figures in the notebook, not claims that charts exist.

Continue to
Practical Test 2 continued

## Slide 13 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 13

Explanation to give
Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.

Worked illustration / lecturer answer
Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.

Misconception to address
A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.

On this slide
Include captions and readable written evidence in the notebook.

Task framing (10.0 total): The ML task is correctly identified, the target named, and regression vs classification correctly chosen and justified.

Data preparation & leakage control (20.0 total): Cleaning and encoding appropriate.

Split made before any fitting.

Continue to
Practical Test 2 continued

## Slide 14 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 14

Explanation to give
Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.

Worked illustration / lecturer answer
Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.

Misconception to address
A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.

On this slide
Pipeline used.

No leakage present - a leak found by the marker caps this criterion at zero.

Modelling protocol (20.0 total): At least two models built and compared under identical conditions.

Baseline included.

Continue to
Practical Test 2 continued

## Slide 15 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 15

Explanation to give
Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.

Worked illustration / lecturer answer
MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.

Misconception to address
Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.

On this slide
Hyperparameters handled sensibly.

Evaluation & metric justification (20.0 total): Correct metrics computed.

Metric choice defended against the cost of error.

Cross-validation reported with a spread, not a single number.

Continue to
Practical Test 2 continued

## Slide 16 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 16

Explanation to give
Read the metric with its unit and evaluation population. Explain why that error measure matches the cost of a wrong decision in the stated engineering setting.

Worked illustration / lecturer answer
MAE 3 kW describes an average absolute error on named observations; it does not guarantee every prediction lies within 3 kW. Report baseline comparison and the evaluation protocol.

Misconception to address
Avoid a deployment claim based only on a score. State genuine limitations involving data coverage, measurement quality or future operating conditions.

On this slide
Engineering interpretation & limits (20.0 total): The result is stated in physical or operational units.

Three genuine limitations given.

A clear position on whether it should be deployed.

Code clarity (10.0 total): Runs top to bottom.

Continue to
Practical Test 2 continued

## Slide 17 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 17

Explanation to give
Explain the order: partition data using the stated protocol, fit preparation on training data, fit models, compare on validation data and leave final test data untouched until choices are fixed.

Worked illustration / lecturer answer
Compare models on identical held-out observations with the same metric and preprocessing rules. Each cross-validation training fold learns its own preparation values.

Misconception to address
A written claim of no leakage must agree with the executable split and fitting code. Follow the published execution requirement for any criterion linked to the split check.

On this slide
Readable.

Commented where the intent is not obvious.

Execution requirement for c2: Data-preparation credit requires the published leakage-safe split check to pass.

If this check fails, written marks in that criterion are zero; other criteria remain independently scored.

Continue to
Practical Test 2 continued

## Slide 18 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 18

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
At the Part A boundary, follow the official snapshot procedure. During the 25-minute Part B period, students type reasoning but must not execute code. Do not change the published timing during an explanation.

On this slide
Timing and Part B

15 minutes setup, 120 minutes practical, 25 minutes typed offline reasoning with code execution prohibited, 20 minutes collection.

No internet, messaging or AI.

Answer: Why your main cleaning/model choice?

Continue to
Practical Test 2 continued

## Slide 19 — Practical Test 2 continued

Practical Test 2 continued
CML3112, Week 14, slide 19

Explanation to give
A chart must answer a stated question and show the actual data result. Explain what one mark represents and label both the quantity and unit before stating the finding.

Worked illustration / lecturer answer
A useful caption names the group or sample, the observed difference and the relevant unit. A limitation states what the plotted observations cannot establish, such as causation or performance at a new site.

Misconception to address
Text claiming “a chart was made” is not the required chart. Check the exact number and kinds required on this slide and in the assessment guide.

On this slide
What can your chart/metric not establish?

What evidence would change your recommendation?

What further data is required?

Invigilated offline collection is authoritative; Google upload is a later transport step and must not impose an internet requirement during the test.

Continue to
Practical Test 2 submission

## Slide 20 — Practical Test 2 submission

Practical Test 2 submission
CML3112, Week 14, slide 20

Explanation to give
This slide hands over CML3112 TEST2. Show the exact form title before uploading. The required packet is one completed .ipynb notebook.

Worked illustration / lecturer answer
For TEST1/TEST2, save Part B under My written evidence. Collect the complete notebook offline under invigilation; the later form upload only transports that collected version.

Misconception to address
Students enter their own Student Registration Number as required freeform text. They wait for filenames to appear, press Submit and keep the confirmation. A file saved in Drive or GitHub is not itself a form submission.

On this slide
Offline invigilated collection is authoritative.

Google upload is a later transport step.

Save one notebook with Part B under My written evidence.

No internet, messaging or AI during the test.

Continue to
Revision and submission checklist

## Slide 21 — Revision and submission checklist

Revision and submission checklist
CML3112, Week 14, slide 21

Explanation to give
Prepare for Test 2 by rehearsing the previously taught modelling decisions and the offline evidence workflow. Do not turn the assessed period into a worked lesson.

Worked illustration / lecturer answer
Part B is typed reasoning in the same notebook, with code execution prohibited. The invigilated collection is authoritative; a later upload only transports that snapshot.

Misconception to address
Close by identifying the actual saved file and its correct submission route. Read the live deadline. For current weekly notebook tasks, students upload their own work, not the practice notebook, ZIP or grading files.

On this slide
You can explain training-only preprocessing and locate your saved evidence.

Save your work and check the required submission files.
