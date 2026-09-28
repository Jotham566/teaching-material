# CML3111 DA_PROJECT: Data analysis project — variant A

Investigate motor winding temperature. Target units: deg C. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.

Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to CML3111.

Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.

Published total: 100 marks. Deterministic component: 42. Written/evidence component: 58.0. Original criterion totals are preserved.

## Engineering questions

What is the cleaned mean target in its unit? Which equipment group has the highest mean, and what is the gap to the lowest? What load/target pattern is visible, and why does it not establish causation?

## Required interfaces

- clean_records(records) — 10 marks within c2. Return copied records in original order: remove repeated record_id after its first occurrence, drop rows with missing target or load_pct outside 0–100 inclusive, then fill missing ambient_c with the median of retained non-missing ambient_c values. Preserve raw input. No other changes.

- summarize_records(clean_records) — 10 marks within c3. Return count, mean, minimum, maximum of target and group_means by equipment_id. Retain full precision.

- build_charts(clean_records) — 12 marks within c3. Return all four figures described by the charts contract, including record_id vs target. These must be actual matplotlib Figure objects, not metadata dictionaries.

- five_findings(clean_records) — 10 marks within c4. Return a dict with count, mean, minimum, maximum and group_gap (highest minus lowest equipment mean). Each value is a dict with value and unit; count uses observations and other values use the cohort target unit. These numerical findings are checked independently of the narrative.

## Full investigation and evidence

Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete every original rubric criterion below, not just the checked functions. Include profiling, justified cleaning, question-led charts and your engineering recommendation where required. Keep raw data. State units and distinguish correlation from causation. Charts must be actual labelled figures in the notebook, not claims that charts exist. Include concise captions and an accessible report.

- Question & dataset fit (20.0 total): A real engineering question is stated, and the chosen dataset can actually answer it. Provenance and licence stated.

- Data quality work (25.0 total): Defects found and handled with written justification. A data quality statement is present.

- Analysis & visualisation (30.0 total): Four or more charts, each answering a stated question. Correct chart types, labelled axes, findings in the captions.

- Findings & interpretation (20.0 total): Conclusions supported by the analysis, stated in engineering terms, with limitations acknowledged.

- Individual contribution log (5.0 total): Present, specific, and consistent with the repository's commit history.

## Submission

Submit one completed notebook and one complete DOCX or selectable-text PDF report together. Include the repository URL, run instructions and required contribution/declaration evidence in the report. Keep repository supporting files, but a URL alone does not supply assessable evidence. Read ASSIGNMENT_INSTRUCTIONS.txt for the full start, check and hand-in steps. Keep local copies. The lecturer must validate grading and release this assessment before issuing it.
