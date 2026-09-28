# CML3111 ML_PROJECT: Engineering ML project — variant A

Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3111.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 100 marks. Deterministic component: 20. Written/evidence component: 80.0. Original criterion totals are preserved.

## Engineering questions

Frame an engineering prediction decision. Compare a baseline and two fitted models under a fixed protocol, document prediction-time features, quantify held-out errors and state conditions of use.

## Required interfaces

- predict_regression(training_records, feature_records) — 10 marks within c3. Fit a training-mean baseline, linear regression and a decision tree (max_depth=4, random_state=17) using load_pct and ambient_c only. Return three prediction lists under baseline, linear and tree. Feature records have no target. Fit preprocessing only on training data.

- group_split(records) — 5 marks within c5. Assign whole equipment groups: E1–E4 to train, E5 to validation, E6 to test. Return train, validation and test lists of record_id in input order. Do not use target values to choose membership.

- regression_errors(actual, predicted) — 5 marks within c5. Return mae and rmse, calculated over the same paired observations, with full precision.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete every original rubric criterion below, not just the checked functions. Include profiling, justified cleaning, question-led charts and your engineering recommendation where required. Keep raw data. State units and distinguish correlation from causation. Charts must be actual labelled figures in the notebook, not claims that charts exist. Include concise captions and an accessible report.

- Problem definition (15.0 total): The engineering problem is real, specific and bounded. The ML task is correctly derived from it. The target variable is justified, not merely available.

- Data understanding (15.0 total): Provenance, licence and collection method stated. Defects found and handled with justification. Limitations of the data acknowledged before any modelling.

- Methodology (20.0 total): Appropriate models chosen and compared under one protocol. Pipeline used. Hyperparameters handled sensibly. Choices explained rather than defaulted to.

- Engineering reasoning (20.0 total): Domain knowledge visibly enters the work through features, banding, metric choice or interpretation. The result is discussed as engineering, not as a score.

- Validation (15.0 total): Correct train/test discipline, cross-validation with a reported spread, leakage explicitly checked and ruled out, metric justified against the cost of error.

- Communication (10.0 total): The 2-page brief is readable by a non-specialist engineer. Charts answer questions and are captioned with findings. Uncertainty and limitations stated honestly.

- Reproducibility & documentation (5.0 total): Repository runs from a clean clone. README complete. requirements.txt present. Seeds set. AI use declared. Contribution log present.

## Submission

Submit one completed notebook and one complete DOCX or selectable-text PDF report together. Include the repository URL, run instructions and required contribution/declaration evidence in the report. Keep repository supporting files, but a URL alone does not supply assessable evidence. Read ASSIGNMENT_INSTRUCTIONS.txt for the full start, check and hand-in steps. Keep local copies. The lecturer must validate grading and release this assessment before issuing it.
