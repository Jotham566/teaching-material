# CML3113 TEST1: Practical Test 1 — variant B

Investigate crusher energy demand. Target units: kWh/t. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3113.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 100 marks. Deterministic component: 52. Written/evidence component: 48.0. Original criterion totals are preserved.

## Engineering questions

What is the cleaned mean target in its unit? Which equipment group has the highest mean, and what is the gap to the lowest? What load/target pattern is visible, and why does it not establish causation?

## Required interfaces

- summarize_records(clean_records) — 10 marks within c1. Return count, mean, minimum, maximum of target and group_means by equipment_id. Retain full precision.

- clean_records(records) — 10 marks within c2. Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values. Preserve raw input. No other changes.

- build_charts(clean_records) — 12 marks within c3. Return at least three actual matplotlib Figure objects: scatter load_pct vs target; bar of mean target by equipment_id in alphabetical order; target histogram with ten equal bins from minimum to maximum. Add chart titles and axis labels, including target units. A fourth figure, when required, plots record_id vs target in input order.

- five_findings(clean_records) — 20 marks within c4. Return a dict with count, mean, minimum, maximum and group_gap (highest minus lowest equipment mean). Each value is a dict with value and unit; count uses observations and other values use the cohort target unit. These numerical findings are checked independently of the narrative.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete every original rubric criterion below, not just the checked functions. Include profiling, justified cleaning, question-led charts and your engineering recommendation where required. Keep raw data. State units and distinguish correlation from causation. Charts must be actual labelled figures in the notebook, not claims that charts exist. Include concise captions and an accessible report.

- Loading & profiling (15.0 total): Data loaded correctly; shape, types and summary produced; the dataset is described accurately in the student's own words.

- Cleaning decisions & justification (20.0 total): Defects found. Each handling decision stated AND justified. Marks are for the justification - an unjustified correct fix scores roughly half.

- Visualisation (20.0 total): Three charts, each captioned with the question it answers. Correct chart type. Axes labelled with units. No decoration without purpose.

- Findings (20.0 total): Five findings, supported by evidence from the data, stated with correct magnitudes and units. A wrong number loses the mark even if the method was right.

- Engineering interpretation (15.0 total): One recommendation that an engineer could act on, plus a clear statement of what further data would be needed.

- Clarity & reproducibility (10.0 total): Notebook runs top to bottom. Logical order. Markdown explains intent. No dead code.

## Timing and Part B

15 minutes setup, 120 minutes practical, 25 minutes typed offline reasoning with code execution prohibited, 20 minutes collection. No internet, messaging or AI. Answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required? Invigilated offline collection is authoritative; Google upload is a later transport step and must not impose an internet requirement during the test.

## Submission

Submit exactly one complete .ipynb containing practical code, chart outputs, written evidence and typed Part B answers. Write Part B under a Part B subheading in the existing text cell beginning ## My written evidence, keeping that exact heading; do not execute code during the reasoning period. The invigilator collects the notebook offline; any later form upload transports that collected work. Do not attach a separate report to the notebook-only test form. Read ASSIGNMENT_INSTRUCTIONS.txt for the full start, check and hand-in steps. Keep local copies. The lecturer must validate grading and release this assessment before issuing it.
