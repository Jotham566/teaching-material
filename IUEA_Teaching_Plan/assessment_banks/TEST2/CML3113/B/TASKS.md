# CML3113 TEST2: Practical Test 2 — variant B

Investigate crusher energy demand. Target units: kWh/t. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3113.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 100 marks. Deterministic component: 30. Written/evidence component: 70.0. Original criterion totals are preserved.

## Engineering questions

Frame the prediction decision, justify group separation and preprocessing, compare a baseline with two fitted models, report errors in target units and state deployment limitations.

## Required interfaces

- group_split(records) — 10 marks within c2. Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test. Return train, validation and test lists of record_id in input order. Do not use target values to choose membership.

- predict_regression(training_records, feature_records) — 10 marks within c3. Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.

- regression_errors(actual, predicted) — 10 marks within c4. Return mae and rmse, calculated over the same paired observations, with full precision.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete every original rubric criterion below, not just the checked functions. Include profiling, justified cleaning, question-led charts and your engineering recommendation where required. Keep raw data. State units and distinguish correlation from causation. Charts must be actual labelled figures in the notebook, not claims that charts exist. Include concise captions and an accessible report.

- Task framing (10.0 total): The ML task is correctly identified, the target named, and regression vs classification correctly chosen and justified.

- Data preparation & leakage control (20.0 total): Cleaning and encoding appropriate. Split made before any fitting. Pipeline used. No leakage present - a leak found by the marker caps this criterion at zero.

- Modelling protocol (20.0 total): At least two models built and compared under identical conditions. Baseline included. Hyperparameters handled sensibly.

- Evaluation & metric justification (20.0 total): Correct metrics computed. Metric choice defended against the cost of error. Cross-validation reported with a spread, not a single number.

- Engineering interpretation & limits (20.0 total): The result is stated in physical or operational units. Three genuine limitations given. A clear position on whether it should be deployed.

- Code clarity (10.0 total): Runs top to bottom. Readable. Commented where the intent is not obvious.

Execution requirement for c2: Data-preparation credit requires the published leakage-safe split check to pass. If this check fails, written marks in that criterion are zero; other criteria remain independently scored.

## Timing and Part B

15 minutes setup, 120 minutes practical, 25 minutes typed offline reasoning with code execution prohibited, 20 minutes collection. No internet, messaging or AI. Answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required? Invigilated offline collection is authoritative; Google upload is a later transport step and must not impose an internet requirement during the test.

## Submission

Submit exactly one complete .ipynb containing practical code, chart outputs, written evidence and typed Part B answers. Write Part B under a Part B subheading in the existing text cell beginning ## My written evidence, keeping that exact heading; do not execute code during the reasoning period. The invigilator collects the notebook offline; any later form upload transports that collected work. Do not attach a separate report to the notebook-only test form. Read ASSIGNMENT_INSTRUCTIONS.txt for the full start, check and hand-in steps. Keep local copies. The lecturer must validate grading and release this assessment before issuing it.
