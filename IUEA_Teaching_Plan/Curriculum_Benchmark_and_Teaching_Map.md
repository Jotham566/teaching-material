# Curriculum benchmark and teaching map

**Teaching-mode update, 29 September 2026:** The Week 3–15 PowerPoints supersede the earlier live pair/activity approach described below. Use direct lecturer demonstrations and individual revision with worked answers. Collections are introduced in Week 3 before indexing and developed in Week 4 before record processing. See the current slide-by-slide lecturer companions for the authoritative sequence.


Reviewed and revised 16 September 2026. Teach with the PowerPoints in `decks/`. The notebook supports practice; the issued assignment remains the graded submission.

## What the benchmark means for our learners

Google’s [Machine Learning Crash Course prerequisites](https://developers.google.com/machine-learning/crash-course/prereqs-and-prework) include Python functions, collections, loops, conditions, basic types and familiarity with NumPy/pandas. We therefore teach these explicitly before model fitting rather than assume them.

[IBM Data Science](https://www.coursera.org/professional-certificates/ibm-data-science) provides a foundation in Python, SQL, analysis and projects. [IBM AI Engineering](https://www.coursera.org/professional-certificates/ai-engineer) is an intermediate pathway. Its advanced model coverage is a later destination, not a reason to rush novice students through programming.

[DeepLearning.AI’s Machine Learning Specialization](https://www.deeplearning.ai/specializations/machine-learning) expects basic coding. Its visual intuition, practice notebooks and supervised-learning progression inform our explain–predict–run–change routine. These course comparisons are teaching benchmarks, not claims of equivalent certification or complete coverage.

[Google Data Analytics](https://grow.google/certificates/data-analytics/) reinforces data types, SQL, analysis and communication. Its current page contains both Python and R descriptions, so language-specific equivalence is not assumed. SQL belongs primarily to the independent Data Analyst track, not an unannounced extra IUEA assessment.

## How the research changed the slides

IBM’s current [Python for Data Science, AI & Development](https://www.coursera.org/learn/python-for-applied-data-science-ai) introduces types and expressions, then collections, control flow, functions, files and libraries through notebook labs. Our sequence follows that prerequisite order. We explicitly unpack symbols, conversions, indexing, dictionary keys, methods and common errors before expecting students to use them. IBM’s later API and class-authoring topics are not added as surprise Semester 1 requirements.

The IES [Organizing Instruction and Study to Improve Student Learning guide](https://ies.ed.gov/ncee/wwc/PracticeGuide/1), published in 2007 and checked again for this review, recommends alternating worked examples with learner problems, pairing graphics with explanations, linking concrete and abstract representations, retrieval practice and explanatory questions. These are evidence-based teaching principles alongside the current industry course comparisons, not a new industry certification standard.

The revised decks implement those principles with larger illustrations, paired concept panels, readable code with syntax explanations, trace tables, prediction pauses, short physical activities and discussion answers. A picture always has an observation or reasoning prompt. Editable slide text and native tables remain available in PowerPoint; illustrations are embedded images. Generated illustrations and their prompts are documented in `figs/experiential/ASSET_SOURCES.md` at the repository root.

## Teaching sequence and evidence of understanding

| Week | Foundation to explain before the task | Learner checkpoint |
|---|---|---|
| 2 | Files, cells, outputs, shared memory, restart, save, repository | Reopen the saved main notebook and explain one output |
| 3 | int/float/str/bool/None, quotes, names, conversion, operators, precedence, if/else, indentation, def, parameters, return | Predict a small calculation and change one function input |
| 4 | Lists, zero-based indexing, slices, append, dictionaries, keys, items, tuples, sets, loops, CSV text conversion | Trace a running total and retrieve a named field |
| 5 | Library imports, aliases, methods, DataFrames, Series, masks, group summaries, units | Explain which rows a mask selects and why |
| 6 | Copies, missing values, duplicate IDs, mean/median, chart selection, optional comprehensions | Justify a cleaning decision while preserving raw data |
| 7 | Previously taught operations and saving both test files | Rehearse before the timed assessment |
| 8 | Array shape, features/target, regression, residual, MAE, training-only preprocessing and baseline | Read a prediction error in the target unit |
| 9 | Binary labels, indicators, probability, threshold, confusion matrix, precision/recall and stated costs | Explain one false negative in the programme’s setting |
| 10 | Group separation, validation, folds, mean/spread, final test isolation | Explain which records may influence model choice |
| 11 | Derived features and physical meaning | Confirm an input exists at prediction time |
| 12 | Fair comparisons and constraints | Apply every requirement before selecting a candidate |
| 13 | Fresh run, paths, environment, README and contribution evidence | Another learner follows the run instructions |
| 14 | Previously taught evaluation and typed reasoning | Rehearse the offline collection procedure |
| 15 | Question, evidence, limitations, individual contribution | Explain one personally contributed decision |

## A manageable three-hour ordinary class

Use about 15 minutes for recall, 45 for explanation and demonstration, 10 for a break, 45 for guided practice, 35 for an individual attempt, 20 for the assignment brief and 10 for an exit check. This is a teaching allocation, not the exam timetable.

The decks include reference explanations and public task contracts. Do not spend equal time on every slide. If learners fail the checkpoint, repeat the smallest example with different values. Move optional extensions to later practice. Reserve time to explain the assessed function names, inputs, return values, required files and closing time.

Use the five-minute pair activity inside the guided-practice allocation, then discuss its answer. It is ungraded and adds no upload or manual marking. Weeks 7 and 14 contain rehearsal activities to complete before the test period.

Use Presenter View for the expected practice results. The illustrated examples use invented or illustrative data. Programme-specific task briefs supply the authoritative data, units and required outputs.

## Concrete activities to make the idea visible

| Week | Action | Connection back to Python or evaluation |
|---|---|---|
| 2 | Act as the notebook memory: 12, add 5, repeat the addition | A cell changes the value retained in the session |
| 3 | Pass 4 and 7 through a “double” instruction | Inputs, a reusable rule and returned answers |
| 4 | Move through paper readings and keep a total/count | A loop updates an accumulator |
| 5 | Sort building cards and add each pile | Grouping and aggregation |
| 6 | Keep a raw copy, remove a repeated ID and label an estimate | Explicit cleaning policy and an audit trail |
| 8 | Calculate a prediction by hand and compare it to a measurement | Prediction, actual value and absolute error |
| 9 | Place paired labels into four cells | TP, FN, FP, TN, precision and recall |
| 10 | Keep cards for the same equipment together | Group separation and a reserved final test |
| 11 | Change one comparison error and recalculate improvement | Evidence for retaining a derived feature |
| 12 | Cross out ineligible candidates before ranking | Inclusive constraints and tie-breaks |
| 13 | Exchange run instructions without giving verbal hints | Reproducibility and actionable feedback |
| 15 | Explain one finding and its limitation to a colleague | Evidence-based communication and contribution |

Use paper already available in class. Each activity has a discussion answer in the deck. Tiny activity data illustrate the method; the issued assignment supplies its own data and rules.

## Assignments and quizzes

The last slides hold the cohort’s assignment and quiz links. Opening a link does not activate a quiz. Activate the matching week/cohort function in Quiz Controls, then announce its exact close time: **24 hours after activation**. Assignment upload dates follow their separate published schedule.

Students use their **Student Registration Number**. Use only fictional examples in demonstrations. Week 2 submits the main notebook and the student’s own README; 01–04 repairs and hello_engineering.py are practice. Later weeks follow the issued brief. Guided practice is not an additional graded upload.

Required function names and outputs are preserved for automatic marking. Students should run visible checks, restart, run all and save before uploading. Weekly numerical/code checks remain deterministic. Written-evidence grading uses the configured local workflow and its release checks. Major projects, tests and demonstrations still require their separate calibration/readiness checks before release.

## Independent Data Analyst track: SQL coverage review

Existing session sources place tables and keys before querying, then SELECT/FROM/WHERE/ORDER BY, aggregates/GROUP BY/HAVING, and INNER/LEFT JOIN with row-count checks. SQL NULL and unmatched rows must be explained before joins; COUNT(*) and COUNT(column) differ when values are NULL. A LEFT JOIN followed by a WHERE condition on the right table can remove unmatched rows. Use the track’s worked examples and public SQL lab rather than add SQL to IUEA’s Python grading interfaces.

The current visual rebuild covers the 41 remaining IUEA decks. The independent track’s existing presentations have not been rebuilt in this pass.

## Later learning

Google Cloud’s [Professional ML Engineer guide](https://cloud.google.com/learn/certification/guides/machine-learning-engineer) extends into production systems, pipelines and ongoing evaluation. Those professional responsibilities inform our emphasis on reproducibility and honest evaluation, while cloud operations remain a later pathway.

Neural networks, deep learning frameworks, deployment, monitoring and production ML engineering need a subsequent pathway after students can reliably prepare data, fit/evaluate a simple model and explain its limitations. Do not turn them into new Semester 1 requirements merely to match an advanced certificate’s topic list.
