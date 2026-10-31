# Machine Learning: curriculum

Eight weeks, three core sessions a week, 24 core sessions, each proposed at three hours including a 15-minute break. Four two-hour foundation labs (F01 to F04) sit on a fourth day in weeks 1 to 4, and an optional extension follows session 24. Audience: S.4 to S.6 students and school leavers. No programming, spreadsheet or statistics experience is assumed. Confirm session length and dates before advertising hour totals.


## Week 1. Python and a first prediction

Product of the week: A first prediction run, a small calculation notebook and F01.

### Session 1. Your first instruction and your first prediction

Question: Can a computer guess a rent after seeing 120 homes?

By the end: you can run, save and reopen a notebook, and you can say what a prediction is using the rent example.

New library: pandas, sklearn.

Words: file, notebook, code cell, output, print, prediction.

Evidence: ML01.ipynb with a nickname, 11, and a rent estimate for 80 square metres, reopened and saved.

### Session 2. Values, names and types

Question: What kind of thing is each part of a sale?

By the end: you can create whole numbers, decimals and text, and predict what happens when a name is given a new value.

Words: value, integer, float, string, variable, type.

Evidence: ML02.ipynb with the total 5001.0 and a sentence explaining the quotation marks.

### Session 3. Arithmetic, converting text and reading errors

Question: How do I turn the text of a price into a number I can calculate with?

By the end: you can calculate with the five basic operators, turn text into a number, and find the line an error points to.

Words: operator, parentheses, comment, convert, error message, traceback.

Evidence: ML03.ipynb with the prediction written first, the result 50.0, and a sentence on division by zero.

Then lab F01, Numbers, names and predicting Python output.


## Week 2. Python you need

Product of the week: A flower rule, a loop and a checked function, plus F02.

### Session 4. Decisions and a hand-written flower rule

Question: How often does a three-line rule name the right flower?

By the end: you can write an if, elif and else decision, test it at its boundary, and count how often a simple rule is right.

Words: comparison, Boolean, if, else, elif, indentation.

Evidence: ML04.ipynb with the ticket decision tested at three budgets and the flower count 7 out of 8.

### Session 5. Lists, dictionaries and loops

Question: How do I repeat one calculation for every item in a list?

By the end: you can read a list position and a dictionary key, and trace a loop that adds up values.

Words: list, index, dictionary, key, loop, item.

Evidence: ML05.ipynb with the three loop outputs, the stock 8, and the count 2.

### Session 6. Functions and checks that fail loudly

Question: How do I turn my flower rule into a reusable tool and test it?

By the end: you can write a function that returns a result, and check it against known answers with assert.

Words: function, parameter, argument, return, assert, check.

Evidence: ML06.ipynb with double defined, three passing asserts, and a clean run from the top.

Then lab F02, Lists, vectors and NumPy arrays.


## Week 3. Tables and statistics

Product of the week: A described table, a revenue column and summary numbers, plus F03.

### Session 7. Tables and reading a CSV file

Question: How many sales are in the practice shop file, and what does each one record?

By the end: you can read a CSV file into a pandas table and say how many rows and columns it has.

New library: pandas.

Words: row and column, header, CSV file, library and import, DataFrame, shape.

Evidence: ML07.ipynb with the first rows, the shape (120, 4), and two sentences on a row and the unit.

### Session 8. Select, filter and calculate new columns

Question: Which item earned the most money in the practice shop?

By the end: you can pick a column, keep rows that meet a condition, add a revenue column and total it by item.

New library: pandas.

Words: select a column, filter, new column, sum, group, revenue.

Evidence: ML08.ipynb with 42 rows, total 247, mean about 5.88, and a sentence on the difference.

### Session 9. Mean, median, range and proportions

Question: What is a typical number of units in a sale, and how spread out are the sales?

By the end: you can calculate the mean, median, range and a proportion, and say which one an extreme value moves most.

New library: numpy.

Words: mean, median, range, percentile, proportion, outlier.

Evidence: ML09.ipynb with mean, median and range for [10, 12, 14, 16] before and after adding 100, and the two rates.

Then lab F03, Variation, proportions and probability.


## Week 4. Clean, chart, question

Product of the week: Checkpoint one with a chart and a project question, plus F04.

### Session 10. Cleaning without hiding evidence

Question: What is wrong with this table, and what did I change?

By the end: you can count missing values and duplicates, remove an exact duplicate on a copy, and save a cleaning log.

New library: pandas.

Words: missing value, duplicate, raw data, cleaning log, to_csv, index=False.

Evidence: ML10.ipynb with the counts 2 missing, 1 duplicate, the saved log, and the explanation about zero.

### Session 11. Charts that show what the numbers say

Question: How do I show which item earns most, and how sales vary, in a picture?

By the end: you can draw a labelled bar chart, a histogram and a box plot, and write one finding and one limitation.

New library: matplotlib, seaborn.

Words: bar chart, histogram, box plot, axis label, title, finding.

Evidence: ML11.ipynb with a labelled bar chart, one finding with a number, one limitation, and the rainfall answer.

### Session 12. Checkpoint one and a project question

Question: Can I take a table from a file to a labelled chart and a careful finding on my own?

By the end: you can load a table, check it, total it, chart it, write two findings and a limitation, and ask one prediction question a table could answer.

Words: checkpoint, reproducible, data dictionary, target, input, limitation.

Evidence: ML12.ipynb: totals, one labelled chart, two findings, one limitation, a missing-value check, a restarted-kernel run, and a three-sentence project question.

Then lab F04, Matrices, weighted sums and slope.


## Week 5. Baselines and a line

Product of the week: A baseline and a fitted line with their errors compared.

### Session 13. Features, targets and an honest baseline

Question: What did the session 1 model learn from, and how well would a plain guess do?

By the end: you can name the features and the target in a table, and calculate a baseline error that any model must beat.

New library: sklearn.

Words: feature, training data, test data, leakage, baseline.

Evidence: ML13.ipynb with baseline 4000.0, error 1000.0, and one named leaked feature.

### Session 14. Predicting a number with a line

Question: How close does a straight line get to the rents of eight homes?

By the end: you can guess a line by hand, measure its error, and compare it with the line scikit-learn fits.

New library: sklearn.

Words: regression, slope, intercept, fit, predict, error.

Evidence: ML14.ipynb with the prediction 350, the four definitions in the student's own words, and the reason 1000 is risky.

### Session 15. A complete regression experiment

Question: Does the rent model beat a plain guess on homes it has never seen?

By the end: you can split data, fit a model and a baseline on the training part, and compare their errors on held-out homes.

New library: sklearn.

Words: train and test split, held-out records, test_size, random_state, baseline model, mean absolute error.

Evidence: ML15.ipynb with both errors, the sentence that the model beats the baseline on held-out homes, and the split unchanged.


## Week 6. Trees and fair tests

Product of the week: Checkpoint two: a tree compared fairly with a locked final test.

### Session 16. Predicting a category with a decision tree

Question: Does a tree that learned its questions beat my hand-written flower rule?

By the end: you can train a small decision tree on iris, read its first question, and compare its accuracy with a baseline and with the hand rule from session 4.

New library: sklearn.

Words: classification, decision tree, class label, accuracy, majority baseline, depth.

Evidence: ML16.ipynb with both accuracies as percentages, the target and one input named, and the sentence about codes.

### Session 17. Mistakes, overfitting and fair comparisons

Question: When is a very high score a warning sign?

By the end: you can read a confusion matrix, spot an overfitted tree from its training and test scores, and explain why the final test must stay locked.

New library: sklearn, matplotlib.

Words: overfitting, confusion matrix, actual and predicted, validation records, final test, locked test.

Evidence: ML17.ipynb with the labelled matrix, 3 right and 2 wrong, and the explanation about tuning on the test.

### Session 18. Checkpoint two with a locked test

Question: Which tree depth is better, and what does a locked test say about it?

By the end: you can split data into training, validation and final test, choose a model on validation only, and report one final test result with its limits.

New library: sklearn.

Words: stratify, validation score, frozen choice, split sizes.

Evidence: ML18.ipynb: split sizes 90, 30 and 30, baseline, two validation scores, the chosen depth, one final test accuracy, a confusion matrix and two limitations.


## Week 7. Your project

Product of the week: An approved plan, a baseline and a compared model.

### Session 19. Project data and a safe plan

Question: Which dataset and which question can I answer with a fair test in two weeks?

By the end: you can describe a supplied dataset, spot a leakage column, and write a seven-heading project plan the instructor can approve.

New library: pandas.

Words: project plan, leakage column, inputs, limits.

Evidence: PROJECT_PLAN.md with seven headings, one named leakage column, and the instructor's approval.

### Session 20. Build the project baseline

Question: How much does a plain guess miss by, before any model helps?

By the end: you can split data into training, validation and locked test, fit a baseline on training only, and draw one descriptive chart.

New library: sklearn, seaborn.

Words: three-way split, baseline error, scatter plot, training only.

Evidence: project.ipynb with the split, the baseline error on validation, one labelled chart, a data dictionary and a cleaning log.

### Session 21. Compare, explain and critique

Question: Does my model beat the baseline fairly, and can I defend each input?

By the end: you can compare candidate models on the same validation rows, explain why one input is excluded, and check a coding assistant's advice with tests.

New library: sklearn.

Words: fair comparison, candidate model, validation error, coding assistant, AI use log.

Evidence: project.ipynb with the baseline error, one candidate model and its validation error, a written decision, and AI_USE_LOG.md.


## Week 8. Hand over

Product of the week: The final test, the report and the unaided demonstration.

### Session 22. The final test and a reproducible handover

Question: How well does my frozen model do on rows nobody has used?

By the end: you can run the final test once, report it separately from validation, and hand over a project that reruns from a restarted kernel.

New library: sklearn.

Words: frozen model, handover, restart and run all, limit.

Evidence: A complete local project folder and a clean rerun from a restarted kernel, with the final test reported once.

### Session 23. Explain the project to a parent

Question: Can a parent say what my model predicts, how I tested it and why it is limited?

By the end: you can explain your project in five minutes with five slides, one demonstration, one chart and one limit, without jargon.

Words: claim, demonstration, audience, backup, disclosure.

Evidence: Five slides saved as showcase.pptx, a PDF or screenshot backup, and a timed rehearsal with feedback.

### Session 24. Parent showcase and next steps

Question: Can I show and explain my own work with nothing to help but what I know?

By the end: you can present your project, explain one decision, make one small code change without AI, and name your next learning goal.

Words: showcase, unaided, completion record, portfolio, next step, feedback.

Evidence: An individual demonstration, one unaided code change, feedback and a recorded completion decision.
