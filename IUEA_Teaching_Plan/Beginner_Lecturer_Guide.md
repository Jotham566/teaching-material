> **Current foundation sequence:** Week 3 now teaches arithmetic and comparisons individually, then traces if/else/elif before functions and list examples. Week 4 teaches for/while, range and loop controls before records. Use the current PowerPoint and slide companion; allow another session when needed rather than skipping an unexplained prerequisite. CML3112’s revised route is in [Week 3 continuation](CML3112_Week3_Continuation.md).

# Teaching from Week 2 onward

Updated 29 September 2026. Week 3–15 decks and their slide-by-slide lecturer companions now follow the revised foundations sequence. For CML3112, resume Week 3 at slide 13 after the twelve already taught slides. See [the continuation notes](CML3112_Week3_Continuation.md).

Open the matching PowerPoint in **decks/** and teach in Slide Show. Use Presenter View for the detailed explanation prompts in speaker notes. Use the cohort student ZIP for practice and the issued assignment. The HTML lesson route is retired. The issued brief remains authoritative for graded outputs.

The slides use illustrated concepts, annotated code and worked examples with answers. Explain them directly; no live pair or role-play activities are required. Students can repeat the examples individually after class using the matching guided notebook. Videos are optional revision. For Weeks 7 and 14, complete rehearsal before the timed test.

The [curriculum benchmark and teaching map](Curriculum_Benchmark_and_Teaching_Map.md) records the research, prerequisite sequence and weekly activities. Definitions and syntax references can be revisited as needed; do not rush through every slide at the same pace.

## A routine that makes understanding visible

Explain the physical example first. Define a new word at its first use, point to the relevant screen item and say each code symbol aloud. Demonstrate one small case, explain a changed case, and leave the matching individual practice for revision. Do not ask only “understood?” or rely on the quickest hands.

Use a hint ladder: (1) restate the input and expected output, (2) trace a smaller example, (3) supply the first step, (4) model an analogous solution and have the learner retry. Use lecturer-led demonstrations in class. Each learner saves and submits their own work. These are ungraded checks, not extra manual marking.

If many learners cannot pass the checkpoint, use the independent-practice recovery time to reteach and defer stretch material. Record the skill to revisit next week. Do not silently reduce published assessment requirements or release an unvalidated assessment.

## Default three-hour teaching timetable

| Elapsed minutes | Activity |
|---|---|
| 00–15 | Recall and access check |
| 15–30 | Explain the physical question and new words |
| 30–50 | Teacher models one small example, including a short optional clip |
| 50–80 | Lecturer demonstrates and traces an analogous example |
| 80–90 | Break |
| 90–125 | Remaining prerequisite explanations and worked examples |
| 125–140 | Bridge from practice to the issued task interfaces |
| 140–165 | Worked revision answers and clarification |
| 165–170 | Explain quiz access and its 24-hour availability window |
| 170–180 | Save, explain requirements and confirm the deadline |

Weeks 7 and 14 use their existing examination timetable; their opening preparation slides are for use before the test, not replacement exam content. Week 15 uses the published demo timetable. Week 13 prioritises studio work and the final weekly quiz. Friday Week 5 has no normal class; announce a supported replacement and retain Week 6 consolidation.

## Follow the prerequisite sequence

Teach in the revised slide order. The guided notebook now follows that same order and identifies the corresponding slide. New terms come before worked use; worked answers follow the explanation; students repeat examples independently after class. Continue a multi-part code example in the same cell and run it only when complete. Keep time for practice rather than treating every slide as a separate lecture.

All 48 IUEA assignment forms now require freeform Student Registration Number text. Students enter their own number exactly as on their record; no pattern is enforced. Existing links and deadlines remain valid. Roster and registered-email matching still apply in grading.

## Video routine

Videos are optional after-class revision; preview the recommended excerpt before sharing it. If time permits in class, play a short excerpt with its listening question. Use captions where available. Allow a student to answer in ordinary language before introducing terminology. Teach the local example if access fails. Watching long tutorials at home is optional, not assumed prior learning.

The supplied GitHub video is 19:53 and uses GitHub Desktop. Use 00:00–02:10 and 03:35–06:08 for the idea of source control. Its originally shared 02:47 start skips that foundation. Keep the browser workflow as the course default.

The supplied Colab tutorial by ProgrammingKnowledge is 22:23: https://www.youtube.com/watch?v=ZdIyMWWGB4U . Its originally shared 17:14 start skips earlier setup. Its description includes GPUs, TPUs, Drive mounting and additional ML libraries. These are not Week 2 requirements. Treat it as optional revision starting at 00:00; select a short cell-running segment only after audiovisual preview. The full transcript did not load during this review, so no exact content verdict is claimed.

## Week 2 Running and saving your first notebook

**Catch-up:** Explain the four tasks separately: A1 and Quiz 1 from Week 1, plus A2 and Quiz 2 from Week 2. Use the cohort links in the slides and Quick Class Checklist. A1 upload shares the A2 deadline; each quiz has its own 24-hour activation window.

**Core:** Each learner runs, explains, restarts, downloads and finds their own main notebook. Create one repository and one useful README using the browser.

**Checkpoint:** Ask everyone to point to the output, rerun one cell, and find the saved .ipynb on their own computer. If they cannot, repeat these actions before GitHub.

**Worked explanation:** Define numbers, values and variables before explaining assignment or notebook memory. Open the extracted proof_of_life.ipynb in Colab. Show the code cell, text cell, run button and output with the pointer before asking students to click. Read each symbol aloud: = stores a value under a name; + adds; print(...) displays its input; parentheses hold the input to print. A # starts a comment for a person. Run the following cells separately. After the first cell, readings refers to 12. The second reads the current value, adds 5, then stores the answer under the same name.

**Practice answer:** 22. Running the entire example from the top resets readings to 12, so a complete run ends at 17 every time.

**Assessment bridge:** Use proof_of_life.ipynb for A2. Upload the cohort CSV into the runtime Files area and show the filename before reading it. Model repair 01, guide 02–03 and trace 04. Submit the completed main notebook and your own README.md together, plus the repository URL. Repairs 01–04 and hello_engineering.py are practice, not extra submissions.

**Defer:** Terminal commands, staging, branching, merging, GitHub Desktop installation and f-string formatting are reference topics. Do not make them prerequisites for A2.

Keep the private IUEA_ML_Week2_Repair_Walkthrough.docx open for exact repairs and each cohort’s filename. The new lesson applies to Friday CML3111/CML3113, not a replacement issue for completed CML3112 work.

**Video:** GitHub Tutorial for Beginners (2025) — https://www.youtube.com/watch?v=v5gnvDUWqFM
00:00–02:10, then 03:35–06:08 (4 min 43 sec total)
Title, channel, 19:53 runtime and chapter boundaries checked on the video page on 15 September 2026. Desktop installation is optional. The originally shared t=167 link starts at installation.

**Next connection:** Week 3 uses the same Colab notebook, but we write small calculations and reusable functions.

**Before the existing quiz:** The number beside a code cell records when it ran in that session, not its position on the page. Restart clears memory; Run All follows page order. A fresh run tests the run order, not whether the engineering formula is valid. A commit is a recorded change. In terminal reference material, git status describes local changes; it does not itself save or upload them.

## Week 3 Python calculations and reusable functions

**Core:** One arithmetic cell, one reusable function and one guarded division explained and modified by each learner; then supported attempts at all five A3 prompts.

**Checkpoint:** Students explain the difference between defining and calling a function, and between return and print. Re-model with double_value if these are confused.

**Worked explanation:** First define numbers, values, variables, types, operators and function calls in the revised slide order. Then work the cohort formula by hand before running its code. State every unit. Use the four-line cohort calculation first; do not begin with formatting, imports or a long function. Introduce one reusable calculation using the example below. Read def, the function name, parentheses, parameter, colon, indentation and return separately. Defining the function does not run its body. Calling double_value(4) supplies 4 for x, calculates 8 and returns 8. The outer print displays it. Then teach an if/else guard with a separate small example.

**Practice answer:** triple_value returns x * 3. The calls give 15 and None respectively. The guard returns before division when people is zero.

**Assessment bridge:** A3 has five named tasks, not five additional projects. Read each public prompt and its exact output name. Signed percentage error = 100 × (measured − expected) / expected. Use a nonzero expected value. For the cohort task: resistive loss = current² × resistance; slab mass = area × thickness × 2400; hydrostatic pressure in kPa = density × 9.81 × depth / 1000. The brief determines which formula you implement. q4 specifies the zero-input behaviour. q5 uses the supplied six readings; trace them on paper, and use your own percentage-error function. Loops are not required yet.

**Defer:** Five-function libraries, module imports, scope details, debugger setup and six independent bug hunts can wait. Demonstrate one ordinary traceback and one unit mistake now.

**Video:** Python Tutorial for Beginners 3: Integers and Floats — https://www.youtube.com/watch?v=khKv-8q7YmY
Opening 00:00–04:00, suggested four-minute excerpt; preview before class
Title/channel and subject confirmed from the original YouTube listing. Exact excerpt content has not been fully watched; keep the local worked example as the fallback.

**Next connection:** Week 4 repeats a calculation for many values using lists and loops.

**Before the existing quiz:** Read the unit beside each function input. Millimetres become metres by dividing by 1000. Percent becomes a fraction by dividing by 100. Rotational speed in rpm becomes radians per second by multiplying by 2π/60. These conversions change the number, not the physical quantity. In an if/elif chain, Python uses the FIRST matching branch. Trace one branch at a time. A TypeError can mean text was used where a number was expected. Put a repeated teaching limit in one clearly named constant.

## Week 4 Lists loops and reading a table

**Core:** Trace one loop, read the actual header and implement one summary together before independent attempts. Give prompts and hints during the investigation.

**Checkpoint:** Students trace the running total without executing and identify the numeric field in the real CSV. Revisit a three-item list if either step fails.

**Worked explanation:** Draw three boxes labelled 0, 1 and 2 holding 2, 4 and 6. Read the first item aloud, then trace the loop by hand. Make a table with columns reading and total: (2,2), (4,6), (6,12). len(readings) counts three items. 12 / 3 is 4. Before a real CSV, show a two-line text extract and name its header. Open the issued CSV together. Explain csv.DictReader as one dictionary per row. Convert only the numeric column and state what should happen to an invalid value.

**Practice answer:** Total 20, count 4, mean 5.0. Resetting inside the loop discards previous additions and leaves only the last value in total.

**Assessment bridge:** Open the issued W04 notebook and its cohort CSV. Compute the requested valid_count, mean_reading, above_limit and group_means using the exact names in the notebook. First identify the correct field and its unit. Keep the CSV beside the notebook locally or upload it into the Colab runtime. The written interpretation is practice.

**Defer:** Nested comprehensions, arbitrary exception handling, a blank-page investigation and data-source hunting are later practice. Never use except: pass to silently erase evidence.

**Next connection:** Week 5 uses pandas to perform the same table operations with less code.

**Before the existing quiz:** DictReader already consumes the header; skipping its first yielded row skips real data. A string such as "unknown" cannot be converted to float. Catch the expected conversion error, count and record it, then continue under a stated policy. Inspect whether skipped rows share a source before reporting a mean. A sample summary describes observed records, not every possible operating condition.

## Week 5 Using pandas to answer table questions

**Core:** Load the issued table and work one selection and grouped total together. Students then attempt the six A5 questions with hints.

**Checkpoint:** Each student predicts a filter and explains what one group total means before running it.

**Worked explanation:** Draw a four-row table before running the example. Describe a reading of kWh as energy, and kW as power; the units are different. Explain dictionary braces, column labels in quotes and lists of values before constructing the DataFrame. In class, read the issued campus_energy.csv with pd.read_csv after this tiny example. Run the column selection, comparison and filtered table in separate cells. Then group rows by building and add energy within each group.

**Practice answer:** Only the row with 7 survives. Building B has the larger total, 12 kWh.

**Assessment bridge:** A5 uses the supplied fictional campus_energy.csv, not a live Kaggle download. Teach read_csv, nunique, division of columns, > filtering, mean and groupby(...).sum().idxmax() before the six public tasks. idxmax returns the label of the largest value. Explain how a rate differs from a total and how a mean of rates differs from a total-cost/total-energy ratio.

**Defer:** NumPy broadcasting, broad Kaggle searches and twelve-plus-ten independent questions are optional extension. No change of editor is needed.

For CML3111/CML3113, publish the recording and issued campus-energy files before the holiday, announce an actual clinic/make-up time and use the first 30 minutes of Week 6 to rehearse loading, filtering and grouping. Do not assume a video has taught the prerequisite.

**Next connection:** Week 6 checks what happens when the data table contains mistakes or gaps.

**Before the existing quiz:** A Boolean mask is a list-like column of True/False values. len(mask) counts all rows; mask.sum() counts True entries. Strings sort as text, so "9" can rank above "100". Inspect numeric types before taking maxima. KeyError often means the column name does not match; check spelling, case and spaces. shape is (rows, columns). Read provenance and units before trusting a dataset.

## Week 6 Cleaning data and explaining changes

**Core:** Trace the cleaning policy on a tiny table, preserve raw input, count changes and explain one limitation. Use a prepared scaffold for the complete published interfaces.

**Checkpoint:** Students distinguish repeated equipment from duplicate records and explain why an outlier is not automatically deleted.

**Worked explanation:** Use the example below to sort four valid readings. The median is (22 + 24) / 2 = 23. Filling a blank with 23 is a stated teaching rule, not a recovered measurement. Model a defect register: observation, evidence, decision, affected count, limitation. Work one repeated record and one missing value together. Draw a scatter plot from four pairs on the board. A pattern can motivate investigation without proving that one variable causes the other.

**Practice answer:** An unusual value alone does not prove an error. The task did not authorize deleting 80. With 26 replacing 24, the middle known values are 22 and 26, so the new fill is 24. The raw list still contains None.

**Assessment bridge:** W06 uses a list of record dictionaries. Show one record and one field lookup before the function interfaces. Parse CSV blank numeric cells as None. Model copying with dict(row) and list.append. Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning. Teach set membership for duplicate IDs and grouped accumulation. Explain that written evidence belongs in My written evidence, not in code comments.

**Defer:** MCAR/MAR/MNAR names, five chart families and six unaided defect hunts are reference. Teach missingness causes in everyday language first.

**Video:** Boxplots are Awesome!!! — https://www.youtube.com/watch?v=fHLhBnmwUM0
Opening up to 04:00, optional preview-selected excerpt
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required; do not make viewing compulsory.

**Next connection:** Week 7 assesses the skills already rehearsed. Complete an offline practice run before test day.

**Before the existing quiz:** Filling blanks with zero changes the mean and may be unjustified. Dropping every row with any blank can remove valid observations. A failed numeric conversion identifies a problematic value to inspect rather than hide. A histogram describes one distribution; a scatter plot shows paired values; a grouped chart compares groups. Read both axes and units. A plausible extreme needs investigation before deletion.

## Week 7 Preparing for Practical Test 1

**Core:** Offline access, familiar interfaces, data reading, valid summaries, reasoning and saving.

**Checkpoint:** Every learner completes the offline save-and-reopen rehearsal. Escalate lab-access failures before the test.

**Worked explanation:** Use this lesson as preparation in Week 6 or a scheduled rehearsal, not as new teaching inside the timed test. Demonstrate one unrelated practice table, one function check and saving a notebook plus the typed Part B document. Use a blank practice packet, never a live test variant. Have every learner locate their files after saving. Confirm the published permitted resources and the failure-reporting procedure.

**Practice answer:** The mean of these three fictional temperature readings is 5 degrees C; three teaching values cannot establish the operating behaviour of real equipment.

**Assessment bridge:** Use the official TEST1 brief, interfaces and rubric. Keep its 145-minute assessment allocation and collection procedure. Release depends on the separate assessment-readiness checks; this practice material does not authorize release.

**Defer:** No new tools, new packages or surprise functions on test day.

**Next connection:** Week 8 introduces a model that learns numerical relationships from examples.

## Week 8 A first prediction model

**Core:** Read the small table, fit a baseline and linear model in separate steps, explain one tree prediction and hand-calculate the two error measures.

**Checkpoint:** Students identify the target, explain why it is absent from prediction inputs and calculate one absolute error.

**Worked explanation:** Use the small invented table below solely to see fit and predict. Real training needs more data, representative evaluation and careful partitioning. A list of lists is a table: each inner list holds the features of one observation. y_train holds one target per training row in the same order. Never reorder one without the other. Read imports and model creation separately. The model line creates an unfitted object. fit learns; predict applies. Explain the shallow tree now because the W08 assignment asks for it, then revisit classification trees in Week 9.

**Practice answer:** Absolute errors are 2 and 4: MAE 3. Squared errors 4 and 16: RMSE sqrt(10), about 3.162. MAE is an average, not an individual error bound.

**Assessment bridge:** W08 asks for baseline, linear and depth-4 tree prediction lists plus error metrics. Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces. Only load_pct and ambient_c are predictors. Introduce grouped partitions now, not first in Week 10. The written comparison is a supplied scenario; do not pretend to have measured its numbers.

**Defer:** Deriving least squares, leaderboard competition, many residual plots and coefficient inference are reference. R² may be negative and is not an accuracy percentage.

**Video:** The Essence of Linear Regression!!! — https://www.youtube.com/watch?v=aFDOzpTeg0s
Opening up to 04:00, optional preview-selected excerpt
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.

**Next connection:** Week 9 predicts a category and counts different kinds of mistakes.

**Before the existing quiz:** A score on training rows describes training fit. A feature table must preserve the training column names, order and units during prediction. A one-dimensional list may have the wrong shape for a model expecting rows and columns. A predicted-versus-actual plot uses the diagonal as perfect agreement; a pattern is not proof of causation. Judge MAE against the baseline and the decision’s acceptable error. R² is not an accuracy percentage.

## Week 9 Classification and the cost of mistakes

**Core:** Correctly label four outcomes, calculate precision/recall/cost and explain a missed-warning trade-off.

**Checkpoint:** Ask students to explain a false negative in their own programme and identify the denominator of recall.

**Worked explanation:** Place four paper observations in a table of actual label and predicted label. Classify each before showing the four-cell matrix. State which axis is actual and which is predicted. Use counts before fractions. The denominator of precision is predicted positives; the denominator of recall is actual positives. Explain what happens if either denominator is zero. Only after the count exercise, show a classifier fit/predict demonstration. Logistic regression predicts a category despite its name. Probability estimates need not be well calibrated.

**Practice answer:** TP=2, FN=0, FP=1, TN=1. Precision 2/3, recall 1, cost 1. This particular change improves recall and cost.

**Assessment bridge:** Implement classification_metrics on arbitrary paired binary labels, not only the example. Use the published zero-denominator convention. Read the supplied W09 comparison separately. Teacher-written cost assumptions are not approved operating limits. All claimed benefits require real-world evaluation.

**Defer:** Three independently built classifiers, ROC/AUC and full threshold curves are extension after the basic matrix is secure.

**Video:** Machine Learning Fundamentals The Confusion Matrix — https://www.youtube.com/watch?v=Kdsp6soqA7o
Opening up to 04:00, optional preview-selected excerpt
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.

**Next connection:** Week 10 asks whether a good-looking validation result can be trusted.

**Before the existing quiz:** A majority-only classifier can achieve high accuracy while missing the rare class. Name the positive class and both confusion-matrix axes. A model expecting numeric features cannot directly use raw category strings; demonstrate one-hot indicators before a fitting example. Compare threshold choices on validation data. Reducing the threshold adds flagged cases and cannot reduce recall on fixed scored observations, but precision can move either way.

## Week 10 Honest validation and leakage

**Core:** Trace whole-group membership, identify one future-information leak and explain training-only preprocessing.

**Checkpoint:** Students explain why E6 cannot be used to choose a feature or tune the tree. If they cannot, revisit the illustrated train/validation/test split.

**Worked explanation:** Write equipment letters on paper cards and distribute whole groups to train, validation and test. Explain why two observations of the same machine can share information. Fit a missing-value replacement on training values [20, 22, 24]: the median is 22. A new hotter observation must not change that fitted median. Show a counterexample: if every input contains a field called final_inspection_result recorded after the outcome, an excellent score can be meaningless for earlier prediction.

**Practice answer:** It stays with B in validation. Mixing a source across partitions can give an overly optimistic estimate for unseen equipment.

**Assessment bridge:** W10 specifies E1–E4 train, E5 validation, E6 test and preserves input order. Use the assigned equipment_id field and record_id outputs. Reuse the W08 fitting pattern. Explain that GroupShuffleSplit and time-based splitting solve different deployment questions; use the rule in the issued task.

**Defer:** Multiple adversarial notebooks, elaborate validation curves and several cross-validation variants are extensions after the core split is understood.

**Video:** Machine Learning Fundamentals Cross Validation — https://www.youtube.com/watch?v=fSytzGwwBVw
Opening up to 04:00, optional preview-selected excerpt
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.

**Next connection:** Week 11 adds one feature and checks whether it helps under the same protocol.

**Before the existing quiz:** Fit an imputer or scaler only on training data; putting it in a Pipeline helps enforce that during cross-validation. A low training error and high validation error suggest overfitting, but data shift or leakage can also matter. Missing predictor values need a stated treatment. Report fold scores and their variation, not just the best fold. Group related observations together when the deployment goal is new equipment.

## Week 11 Creating and testing a useful feature

**Core:** Create one feature, name its unit and interpret one controlled comparison.

**Checkpoint:** Students explain why the largest-looking feature or the most complex model need not improve predictions.

**Worked explanation:** Begin with a percentage: 40% means 40 / 100 = 0.4. Converting percentage to fraction changes units but adds no new information. An interaction may help a simple model express a relationship, but usefulness is tested rather than assumed. An interaction involving Celsius is an empirical feature, not automatically a physical law. Read a two-row results table: base MAE 3, extended MAE 2.5 gives improvement 0.5 target units. Ask which other experimental choices must stay fixed.

**Practice answer:** Improvement is -0.4. This validation comparison does not support retaining it. One split is limited evidence; the final test remains untouched.

**Assessment bridge:** W11 names four output features and a two-model ablation. Explain output order, preservation of input rows, full precision and training-only fitting. Use the supplied written scenario for the interpretation requested there. Do not substitute this practice example’s result.

**Defer:** Five independent features, a full ColumnTransformer construction and domain-code features are extension. Never invent engineering limits.

**Next connection:** Week 12 chooses a model under error, speed and explanation requirements.

**Before the existing quiz:** Rescaling an input usually does not change the partitions available to an ordinary decision tree. An identifier or a future-known field can create an apparent improvement without useful predictive information. Dividing by zero can produce infinity or an error; decide what the denominator means before replacing it. Read ablation differences using the same error definition, and explain features using domain knowledge.

## Week 12 Choosing and explaining a model

**Core:** Apply eligibility and tie-break rules by hand, implement them, and justify a recommendation with a limitation.

**Checkpoint:** Students justify a valid simple model over a more accurate but ineligible one, and distinguish local explanation from global importance.

**Worked explanation:** Cross out ineligible candidates before ranking errors. Then apply the tie-break rule, rather than choosing the most sophisticated model. Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection. A sorted list key can be a tuple: first metric, then speed, then name. Write a short recommendation: question, fair comparison, chosen candidate, reason, limitation and what new evidence could change the choice.

**Practice answer:** The third model. Both eligible models have error 3, but 1 ms is faster than 2 ms.

**Assessment bridge:** W12 uses fields name, validation_mae and latency_ms. Meet both inclusive constraints, then rank by error, latency and alphabetical name. Return None if no candidate qualifies. Complete the error function and interpret the separately supplied scenario. Keep project comparisons and graded interfaces distinct.

**Defer:** A large grid search, four new model implementations and an adversarial defence are optional practice. They must not crowd out the core decision process.

**Video:** Machine Learning Fundamentals Cross Validation — https://www.youtube.com/watch?v=fSytzGwwBVw
Opening up to 04:00, optional preview-selected excerpt
Linked by the official StatQuest video index. Full audiovisual preview and excerpt timing still required.

**Next connection:** Week 13 makes the whole project understandable and runnable by another person.

**Before the existing quiz:** Compare the same metric on the same validation cases with the same preprocessing rules. A small difference needs context, including variation across splits. Code run out of order can overwrite the variable holding a model; restart and run from the top. A local explanation addresses one prediction; global importance summarises many. A post-hoc explanation of a complex model is not its directly readable internal rule.

## Week 13 Making the project understandable and runnable

**Core:** Fresh run, clear README, data provenance, contribution evidence and an independent run check.

**Checkpoint:** A fresh run following the written instructions locates the data and reproduces the result.

**Worked explanation:** Demonstrate a clean run from a fresh session with the actual files. If a variable exists only from an earlier manual cell run, fix the run order. Explain every dependency and test a relative path. Include data-access instructions if the data cannot be redistributed. Model actionable feedback: “Step 2 names data.csv, but the supplied file is readings.csv; please make them match.”

**Practice answer:** Revise that step and repeat. A claim that the notebook runs is supported by a fresh run, not by saved outputs alone.

**Assessment bridge:** No new weekly assignment. Continue the official project deliverables and Week 13 quiz. Rehearse offline TEST2 saving and the published function interfaces before Week 14. Do not add an extra upload.

**Defer:** Package refactoring, complex repository layout and extra tooling are optional. Keep a working simple notebook.

**Video:** GitHub Tutorial for Beginners (2025) — https://www.youtube.com/watch?v=v5gnvDUWqFM
00:00–02:10, then 03:35–06:08 (4 min 43 sec total)
Title, channel, 19:53 runtime and chapter boundaries checked on the video page on 15 September 2026. Desktop installation is optional. The originally shared t=167 link starts at installation.

**Next connection:** Week 14 assesses the modelling and reasoning skills already rehearsed.

**Before the existing quiz:** An absolute path from your own computer will usually fail elsewhere. A relative path starts from the current working folder. Record dependencies and actual versions, and fix randomness where appropriate; identical results across all machines are not guaranteed by a seed alone. Captions should state a supported finding and its scope. Remove conflicting cell assignments and verify a fresh run before submission.

## Week 14 Preparing for Practical Test 2

**Core:** Rehearse already taught processes, file saving and technical failure reporting.

**Checkpoint:** Each learner can save and reopen both required file types in the offline setting.

**Worked explanation:** Use this preparation before the test. Do not consume timed assessment minutes introducing new syntax. Rehearse the actual notebook and typed-document save procedure on the provisioned lab machine using separate practice values. Review one error calculation and one leakage explanation. An unexplained high score is not enough evidence of a useful engineering model.

**Practice answer:** Training data fit the imputer; validation/development data support selection. The final test is kept out of both.

**Assessment bridge:** Use TEST2’s official brief, interfaces, time allocation, permitted resources and packet requirements. Confirm calibrated grading, lab readiness and controlled collection before release.

**Defer:** No new libraries, algorithms or environment installation on test day.

**Next connection:** Week 15 presents the project and explains individual contributions.

## Week 15 Presenting the project and individual contribution

**Core:** Explain the problem, evidence, limitation and individual contribution accurately.

**Checkpoint:** Each student can explain one decision they personally worked on and point to its evidence.

**Worked explanation:** Model a six-minute presentation: one minute for the problem, one for the data, two for the method and result, one for limitations and one for contribution and next step. Explain each chart’s axes and unit before stating its finding. Use the actual measured validation results and state how they were obtained. Practise saying “I do not know yet” followed by the evidence needed to resolve the question. Do not claim deployment readiness from a teaching dataset.

**Practice answer:** A clear explanation names what was measured, what was predicted, how wrong the predictions were and what the result cannot establish.

**Assessment bridge:** Use the published project and DEMO requirements. Each individual submits their own typed defence and reflection through the designated route. Live questioning and peer comments support learning; they are not a new manual marking workload.

**Defer:** New models and a last-minute redesign are unnecessary. Fix broken run instructions first.

**Next connection:** Use the reflection to choose specific revision goals before Semester 2.

## Correctness points to reinforce

- Week 2: do not teach Git staging/terminal vocabulary as a prerequisite to saving in the browser. Kernel counters show execution order, not proof of correctness.
- Week 3: use Colab throughout. State DC assumptions for P=VI. Treat crack, grade-routing and motor alarm limits as fictional examples unless backed by the relevant project specification. A successful run does not validate physical units.
- Week 4: provide a guided CSV example and hints. A blank-page investigation is not the core path for this group.
- Week 5: use the supplied campus-energy data for the assessed tasks. Public anchor datasets are separate extension work. NumPy broadcasting and public notebook searching are not prerequisites.
- Week 6: equal values do not always prove duplicate observations. Use record identity and the published cleaning rule. Missingness mechanisms cannot usually be diagnosed from a small table alone.
- Week 8: distinguish the regression target from Week 9 failure classification. MAE is not a ± prediction interval. Teach the required tree and preprocessing now; the small practice data do not establish real-world predictive performance.
- Week 9: threshold reduction does not guarantee precision decreases at every step. Most importantly, name the positive label and matrix axes. Synthetic warning labels are not observed equipment failures.
- Weeks 10–12: use validation/CV for selection, and reserve the final test. Do not repeatedly choose features or models on “held-out test” scores. Use grouped splits for unseen equipment. Fold-score standard deviation is not a confidence interval.
- Week 13: the working directory determines relative paths. Fixed seeds do not guarantee identical results across all library/hardware changes. Teach only the tested environment route.
- Weeks 7/14/15: keep official assessment formats and deadlines. A teaching review does not resolve the separate pending calibration/collection readiness of major assessments.

## Source and review limits

The 41 in-scope PowerPoint decks now provide the revised teaching sequence. Open the files in decks/ using their existing names. Speaker notes give explanations, practice answers and source references. Student ZIPs contain the guided practice notebook and issued assignment, with no HTML lesson. Major assessment grading and release checks remain separate from slide readiness.

Video title/channel and author-index verification is distinguished from full audiovisual review. Optional clips marked preview-required have not been certified frame by frame. Preview before the class.


## Visual teaching edition

Use the current PowerPoints in `decks/`. The early slides now explain prerequisite syntax with worked examples and illustrations. The matching guided notebook includes the new code examples. Use the [curriculum teaching map](Curriculum_Benchmark_and_Teaching_Map.md) for prerequisite checkpoints and a three-hour teaching allocation. Reserve the final part of class for the issued assignment and its submission link.
