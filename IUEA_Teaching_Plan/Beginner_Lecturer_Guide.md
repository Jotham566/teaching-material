> **Current foundation sequence:** Week 3 now teaches arithmetic and comparisons individually, then traces if/else/elif before functions and list examples. Week 4 teaches for/while, range and loop controls before records. Use the current PowerPoint and slide companion; allow another session when needed rather than skipping an unexplained prerequisite. CML3112’s revised route is in [Week 3 continuation](CML3112_Week3_Continuation.md).

# Teaching from Week 2 onward

Updated 29 September 2026. Week 3–15 decks and their slide-by-slide lecturer companions now follow the revised foundations sequence. CML3112 completed all Week 3 content on 29 September and moves to Week 4. CML3111 and CML3113 have not covered Week 3 and start at slide 1. See [current teaching progress](Teaching_Progress.md).

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

## Weeks 6 to 15 pandas continuation

Updated 15 October 2026. Use the current PowerPoint and matching slide companion. Keep students working with DataFrames for tables after Week 5.

### Week 6

Read the issued CSV with pandas. Inspect missing values and duplicates, preserve raw data, apply the stated cleaning order, summarise and label charts.

### Week 7

Rehearse the offline pandas workflow and the issued function interfaces before test day. Preserve the published examination procedure.

### Week 8

Select named feature columns and targets from DataFrames. Fit a mean baseline, linear model and tree with training-only preprocessing. Compare paired errors.

### Week 9

Use pandas masks to count paired classification outcomes. Explain precision, recall, a threshold and the stated error costs.

### Week 10

Filter equipment groups into separate DataFrames. Fit preprocessing only on training rows and interpret variation across validation folds.

### Week 11

Create derived DataFrame columns. Compare base and extended features on the same validation observations.

### Week 12

Filter candidate tables by both constraints, sort by the published tie-breaks and return the selected name or None.

### Week 13

Reproduce the pandas notebook from a fresh session using documented data paths, dependencies and run order.

### Week 14

Rehearse named-column model inputs, training-only pipelines and the issued return types before Practical Test 2.

### Week 15

Present the reproducible pandas and modelling workflow, supported findings, limitations and individual contribution.

The assignment loader is supplied. Existing function names, returned Python types and marks remain unchanged. Use pandas internally and convert at the return boundary. Correct older solutions remain valid. Lecturer-only pandas reference solutions are checked against the same unseen grading cases and never belong in student ZIPs.

The detailed explanations, example results and misconceptions are in [the slide companions](decks/LECTURER_NOTES_INDEX.md). Share a freshly extracted current ZIP; do not reuse an older extracted folder.
