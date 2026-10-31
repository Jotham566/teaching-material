# Eight week teaching and practice plan

Each track has 24 core classes. ML adds four foundation labs on separate days in weeks 1–4. Keep the three core classes in numbered order and insert each ML lab after that week’s third core class. This is a relative plan; exact dates and holiday breaks are not confirmed.

Core classes propose 180 minutes including a 15-minute break; ML labs propose 120 minutes including a 10-minute break. Confirm session lengths before booking. Do not increase contact-hour claims by counting homework.

## Weekly rhythm and practice

Two 45–60 minute practice blocks on non-class days are the starting allowance. The short repeat-and-change exercise in each lesson is part of these blocks, not additional homework. If stuck for 30 minutes, record the attempted step and question. Weeks 1–6 portfolios use the existing 20% total weight; checkpoints and projects retain their separate weights.

### Week 1: core sessions 01–03

Change two quantities in the arithmetic example, predict the result on paper, then run and explain it. Save the notebook and a short note about one error you repaired.

F01 after ML03.

### Week 2: core sessions 04–06

Change the function inputs, test zero and one ordinary value, then trace a loop over three items. Explain one list index and one dictionary key.

F02 after ML06.

### Week 3: core sessions 07–09

Create a small table with the taught columns, filter one condition and reconcile its grouped total. Compare mean and median before and after an extreme value. DA also calculates a percentage with its denominator.

F03 after ML09.

### Week 4: core sessions 10–12

Finish the taught cleaning log and labelled chart. Rerun checkpoint one; write two traceable findings and one limitation. Keep a copy of the submission.

F04 after ML12.

### Week 5: core sessions 13–15

ML: explain the baseline and check one prediction error by hand. DA: write and save a filter and grouped SQL query, then compare labelled totals with pandas.

No extra lab.

### Week 6: core sessions 16–18

Finish checkpoint two. Explain one model/split mistake (ML) or join/count discrepancy (DA). Repair the method rather than replacing a number by hand.

No extra lab.

### Week 7: core sessions 19–21

Build the approved project incrementally. Save the independent attempt before any supervised AI critique. Keep the separate assistance log; reconcile every reported number.

Supervised AI literacy in Session 21.

### Week 8: core sessions 22–24

Rerun and hand in the project at Session 22; prepare five slides and a backup. Rehearse an unaided explanation and a small code change before Session 24.

Optional modern-AI orientation in Session 23.

## Class objectives and evidence

Open the matching student sheet and instructor guide for the definition, worked example, expected output, independent task, repair cue and full pacing. The independent task is the exit evidence for each objective below. For SQL sessions, run SQL in DB Browser, not a Python code cell.

## ML core classes

### ML01 — Files and your first instruction

By the end: Open, run, save and reopen a notebook; distinguish a text cell from a code cell.

In-class exercise and evidence: Run the two lines. In a new code cell display your chosen nickname and the result of 7 + 4. Save as ML01.ipynb, close it and reopen it.

### ML02 — Values names and data types

By the end: Create and identify integer, float, string and Boolean values; predict how an assignment changes a variable.

In-class exercise and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence explaining why "2500.5" is different.

### ML03 — Arithmetic input and useful errors

By the end: Calculate with taught operators, convert a numerical input and explain a simple error.

In-class exercise and evidence: Convert "12.5" to a number and calculate the price of four items. Predict the result before running. Explain why division by zero cannot be used.

### ML04 — Decisions and true or false

By the end: Trace an if/else decision and change its condition without breaking indentation.

In-class exercise and evidence: Write a decision for a ticket costing 5000: print "Buy" if budget is at least 5000, otherwise "Save". Test 4999, 5000 and 5001.

### ML05 — Lists dictionaries and repetition

By the end: Read list positions and dictionary keys; trace a loop and explain each output.

In-class exercise and evidence: Make a list [2, 4, 6]. Print each value plus 1 using a loop. Make a dictionary with keys name and stock; print the stock. Explain position 0.

### ML06 — Reusable functions and a first check

By the end: Write a function with a return value and check three known inputs using assert.

In-class exercise and evidence: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2). Save the notebook and run all cells from the start.

### ML07 — Tables files and importing a library

By the end: Build a small DataFrame, identify rows/columns and round-trip it through CSV.

In-class exercise and evidence: Create a two-row table with columns item and price_ugx. Save it to prices.csv and read it back. Write the unit in the column name.

### ML08 — Selecting filtering and summaries

By the end: Filter records, group totals and distinguish a total from an average; calculate a derived column.

In-class exercise and evidence: Using the same table, keep rows with units >= 3. Calculate the total units and the mean units per row. Explain why these are different quantities.

### ML09 — Mean median and describing variation

By the end: Calculate mean, median and range and explain the effect of an extreme observation.

In-class exercise and evidence: Calculate mean, median and range for [10, 12, 14, 16]. Add 100 and recalculate. Which summary changes most? Explain using the numbers.

### ML10 — Cleaning without hiding evidence

By the end: Identify missing data and a known accidental duplicate while preserving raw data and a cleaning log.

In-class exercise and evidence: Write a cleaning log: four raw rows, one removed duplicate, one remaining missing price. Explain why replacing the missing price with zero would change the meaning.

### ML11 — Charts and cautious findings

By the end: Create a labelled bar chart from a table and state a supported finding and a limitation.

In-class exercise and evidence: Make the same chart for [6, 9, 4]. Write one numerical finding and one limitation. Select an appropriate chart for daily rainfall and explain why.

### ML12 — Checkpoint one and project question

By the end: Combine taught table, calculation and chart skills; state one feasible prediction question.

In-class exercise and evidence: Submit ML12.ipynb with row count, revenue totals, one chart, two findings and one limitation. Add a three-sentence project proposal: question, supplied dataset, target to predict.

### ML13 — Examples targets and an honest baseline

By the end: Name features and target, separate training/validation/test roles and calculate a simple baseline error.

In-class exercise and evidence: For training values [2000, 4000, 6000], predict one new value using the mean baseline. If its actual value is 5000, compute absolute error. Name a leaked feature when predicting a selling price.

### ML14 — Predicting a number with a line

By the end: Fit the demonstrated regression and explain its numerical prediction and limitation.

In-class exercise and evidence: Predict at input 35. Explain the meaning of X, y, fit and predict in your own words. Why is predicting at 1000 risky?

### ML15 — A complete regression experiment

By the end: Compare a regression model with a training-only baseline using the same held-out records and error measure.

In-class exercise and evidence: Run the example and record the two MAEs. Explain whether the model beats the baseline on these held-out records. Keep the split unchanged; do not keep changing seeds to obtain a better score.

### ML16 — Predicting a category with a tree

By the end: Train a small classification tree and connect category codes with their actual names.

In-class exercise and evidence: Convert both accuracy proportions to percentages. Name the target and one input. Explain why species code 2 does not mean twice species code 1.

### ML17 — Mistakes overfitting and fair comparisons

By the end: Read a confusion matrix and distinguish validation choices from a final test.

In-class exercise and evidence: Draw the 2 by 2 matrix and label both axes. Count correct and incorrect predictions. Explain why trying many settings against final test answers weakens the test.

### ML18 — Checkpoint two with a locked test

By the end: Produce an auditable train/validation/test comparison and explain the frozen final choice.

In-class exercise and evidence: Submit ML18.ipynb: split sizes, baseline, two validation scores, chosen depth, final test accuracy, confusion matrix, and two limitations. Explain your decision without claiming the highest score proves universal superiority.

### ML19 — Project data and a safe plan

By the end: Write a narrow project plan with source, target, available inputs, baseline and evaluation method.

In-class exercise and evidence: Write PROJECT_PLAN.md using those seven headings. Identify one potential leakage column and exclude it. Ask the instructor to approve scope before building.

### ML20 — Build the project baseline

By the end: Implement the project baseline and demonstrate that test answers were not used during training.

In-class exercise and evidence: Complete baseline and one descriptive chart. Submit the notebook, data dictionary and cleaning log. If no cleaning was needed, record the checks rather than inventing changes.

### ML21 — Build compare and explain a model

By the end: Compare the candidate with its baseline, inspect errors and critique a separate coding-assistant hint.

In-class exercise and evidence: Add model code, validation score and a short decision to project.ipynb. Ask a partner to identify the target and baseline from your notebook without help.

### ML22 — Final test and reproducible handover

By the end: Rerun the complete notebook from a fresh kernel and hand over final-test evidence and a report.

In-class exercise and evidence: Use the project checklist. Reopen submitted files. Submit project.ipynb, your data dictionary and report.pdf or report.docx together; use the instructor-issued collection route.

### ML23 — Explain the project to a parent

By the end: Explain the project to a nontechnical listener in five minutes using five clear slides.

In-class exercise and evidence: Practise defining prediction, feature and target without jargon. Prepare a screenshot backup for the demonstration and disclose where AI assistance was used.

### ML24 — Parent showcase and next steps

By the end: Demonstrate, explain and modify a small part of the project without AI assistance.

In-class exercise and evidence: Present your project, acknowledge help, and choose one next learning goal. Keep your project folder and feedback after camp. Demonstrate and explain your work without AI assistance. Close assistant windows and disable generative suggestions; answer an instructor-chosen code question unaided.

## DA core classes

### DA01 — Files and your first instruction

By the end: Open, run, save and reopen a notebook; distinguish a text cell from a code cell.

In-class exercise and evidence: Run the two lines. In a new code cell display your chosen nickname and the result of 7 + 4. Save as DA01.ipynb, close it and reopen it.

### DA02 — Values names and data types

By the end: Create and identify integer, float, string and Boolean values; predict how an assignment changes a variable.

In-class exercise and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence explaining why "2500.5" is different.

### DA03 — Arithmetic input and useful errors

By the end: Calculate with taught operators, convert a numerical input and explain a simple error.

In-class exercise and evidence: Convert "12.5" to a number and calculate the price of four items. Predict the result before running. Explain why division by zero cannot be used.

### DA04 — Decisions and true or false

By the end: Trace an if/else decision and change its condition without breaking indentation.

In-class exercise and evidence: Write a decision for a ticket costing 5000: print "Buy" if budget is at least 5000, otherwise "Save". Test 4999, 5000 and 5001.

### DA05 — Lists dictionaries and repetition

By the end: Read list positions and dictionary keys; trace a loop and explain each output.

In-class exercise and evidence: Make a list [2, 4, 6]. Print each value plus 1 using a loop. Make a dictionary with keys name and stock; print the stock. Explain position 0.

### DA06 — Reusable functions and a first check

By the end: Write a function with a return value and check three known inputs using assert.

In-class exercise and evidence: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2). Save the notebook and run all cells from the start.

### DA07 — Tables files and importing a library

By the end: Build a small DataFrame, identify rows/columns and round-trip it through CSV.

In-class exercise and evidence: Create a two-row table with columns item and price_ugx. Save it to prices.csv and read it back. Write the unit in the column name.

### DA08 — Selecting filtering and summaries

By the end: Filter records, group totals and distinguish a total from an average; calculate a derived column.

In-class exercise and evidence: Using the same table, keep rows with units >= 3. Calculate the total units and the mean units per row. Explain why these are different quantities.

### DA09 — Mean median and describing variation

By the end: Calculate mean, median and range and explain the effect of an extreme observation.

In-class exercise and evidence: Calculate mean, median and range for [10, 12, 14, 16]. Add 100 and recalculate. Which summary changes most? Explain using the numbers. Compare 12 successes out of 20 with 15 out of 50. Calculate each percentage and explain why the larger count need not mean the better rate.

### DA10 — Cleaning without hiding evidence

By the end: Identify missing data and a known accidental duplicate while preserving raw data and a cleaning log.

In-class exercise and evidence: Write a cleaning log: four raw rows, one removed duplicate, one remaining missing price. Explain why replacing the missing price with zero would change the meaning.

### DA11 — Charts and cautious findings

By the end: Create a labelled bar chart from a table and state a supported finding and a limitation.

In-class exercise and evidence: Make the same chart for [6, 9, 4]. Write one numerical finding and one limitation. Select an appropriate chart for daily rainfall and explain why.

### DA12 — Checkpoint one with Python and pandas

By the end: Produce a reproducible sales analysis with reconciled totals, a labelled chart and cautious findings.

In-class exercise and evidence: In DA12.ipynb calculate total units, total revenue and revenue by item. Make one labelled chart and write two findings plus one limitation in text cells. Record missing-value checks and any cleaning actually needed. Run all cells from a restarted kernel, save and submit DA12.ipynb with a short report.pdf or report.docx using the instructor-issued route.

### DA13 — Databases and your first SQL query

By the end: Run SELECT/FROM on the supplied database and save a query with chosen columns.

In-class exercise and evidence: Open camp_shop.sqlite in DB Browser for SQLite. Choose Execute SQL, type the example and run it. Write a query returning sale_id, item and unit_price_ugx.

### DA14 — SQL filters and ordering

By the end: Use WHERE, AND, ORDER BY and LIMIT and explain which rows remain.

In-class exercise and evidence: List Juice records with units at least 4, sorted by units descending then sale_id ascending. Return sale_id, item and units.

### DA15 — SQL totals and groups

By the end: Group SQL results and reconcile SUM and COUNT with corresponding pandas totals.

In-class exercise and evidence: Calculate total units and number of sales records per item. Name the columns total_units and record_count. Compare with your pandas groupby result.

### DA16 — Joining two tables carefully

By the end: Join on a key, check row counts and explain how duplicate keys could inflate revenue.

In-class exercise and evidence: Join category to sales, then calculate revenue by category. Compare the grand total before and after the join.

### DA17 — Nulls validation and repeatable work

By the end: Check NULLs and row counts and save repeatable validation queries.

In-class exercise and evidence: Write queries counting records, checking missing item names and calculating total revenue. Save queries.sql with a comment before each check.

### DA18 — Checkpoint two across Python and SQL

By the end: Compare labelled SQL and pandas results, reconcile grand totals and explain a join risk.

In-class exercise and evidence: Submit DA18.sql, results.csv, DA18.ipynb and a short explanation of your row-count, null and total checks. Explain one join-risk example.

### DA19 — Project question and evidence plan

By the end: Define three descriptive questions answerable from the approved dataset and name their measures.

In-class exercise and evidence: Write PROJECT_PLAN.md. List the raw file, measures, charts, SQL queries and limitations. Ask the instructor to approve a narrow scope.

### DA20 — Build a reliable analysis

By the end: Build a reproducible Python analysis with SQL evidence and a justified cleaning log.

In-class exercise and evidence: Complete the calculation layer and ask a partner to rerun one SQL query. Save feedback and fix the first unexplained discrepancy.

### DA21 — Build and test the project chart report

By the end: Produce a readable chart report and critique a separate coding-assistant hint with tests.

In-class exercise and evidence: Give a peer 30 seconds to find the largest category and total. Record where they hesitate and simplify the notebook headings. To include a chart in the report, call plt.savefig("revenue.png", bbox_inches="tight") before plt.show(). savefig writes the image; bbox_inches="tight" includes labels. Insert the saved PNG into the report using Insert > Pictures/Image.

### DA22 — Write the report and package the evidence

By the end: Hand over a cleanly rerunnable notebook, SQL, source data reference, dictionary and findings report.

In-class exercise and evidence: Submit project.ipynb, queries.sql, cleaning_log.md and report.pdf or report.docx. Include your data dictionary. Check every file opens and the totals agree.

### DA23 — Rehearse a five minute explanation

By the end: Explain a chart, its calculation and a limitation to a nontechnical listener in five minutes.

In-class exercise and evidence: Practise answering: where did this number come from, what did you clean, and what cannot this data tell us? Disclose help and AI use.

### DA24 — Parent showcase and next steps

By the end: Demonstrate, explain and modify a small calculation or query without AI assistance.

In-class exercise and evidence: Present your project and name one next skill to practise. Keep the final files and feedback in your own folder. Demonstrate and explain your work without AI assistance. Close assistant windows and disable generative suggestions; answer an instructor-chosen code question unaided.

## Supporting material and delivery gates

Use the supplied synthetic CSV/SQLite files and DATA_DICTIONARY.md; ML additionally uses the bundled iris teaching dataset. See FOUNDATION_LABS.md for F01–F04, ASSESSMENT_AND_SHOWCASE.md for weights and PROJECT_RUBRIC.md for marking anchors. AI_USE_POLICY.md applies from the first class.

Before teaching, pilot a Python foundations session and a pandas session with a beginner, preflight the actual laptops, test the private hand-in route and calibrate grading on sample submissions. Existing executable reference checks cover numerical work, but a deployed school submission/autograding service and finished PowerPoint course are still outstanding. Do not claim automatic end-to-end marking is operational.
