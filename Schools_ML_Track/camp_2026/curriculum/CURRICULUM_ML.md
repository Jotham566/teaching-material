# Machine Learning: curriculum

Eight weeks, three core sessions a week, 24 core sessions, each proposed at three hours including a 15-minute break. Four two-hour foundation labs (F01 to F04) sit on a fourth day in weeks 1 to 4, and an optional extension follows session 24. Audience: S.4 to S.6 students and school leavers. No programming, spreadsheet or statistics experience is assumed. Each week ends with a badge on the learner's My_Progress_Map.pdf. Every session has a "Where this is used" hook, and every learner grows one personal project from week 1. Confirm session length and dates before advertising hour totals.


## Week 1. Python and a first prediction (badge: First Prediction)

Product of the week: A first prediction run, a small calculation notebook and F01.

### Session 1. Your first instruction and your first prediction

Question: Can a computer guess a rent after seeing 120 homes?

Where this is used: Property apps and agents guess a fair rent from the size and area of a home. A model does the same after studying homes that were already rented, and today you build the smallest version. What rent would you guess for a home you know?

By the end: you can run, save and reopen a notebook, and you can say what a prediction is using the rent example.

New library: pandas, sklearn.

Words: file, notebook, code cell, output, print, prediction.

Saved in your build log: ML01.ipynb with a nickname, 11, and a rent estimate for 80 square metres, reopened and saved.

### Session 2. Values, names and types

Question: What kind of thing is each part of a sale?

Where this is used: A mobile money app keeps the amount as a number and the phone number as text. Mixing them up would cause real mistakes. What would go wrong if an app added two phone numbers together?

By the end: you can create whole numbers, decimals and text, and predict what happens when a name is given a new value.

Words: value, integer, float, string, variable, type.

Saved in your build log: ML02.ipynb with the total 5001.0 and a sentence explaining the quotation marks.

### Session 3. Arithmetic, converting text and reading errors

Question: How do I turn the text of a price into a number I can calculate with?

Where this is used: Anything you type into a form arrives as text. The app has to turn it into a number before it can add, compare or charge. Where in the apps you use does text quietly become a number?

By the end: you can calculate with the five basic operators, turn text into a number, and find the line an error points to.

Words: operator, parentheses, comment, convert, error message, traceback.

Saved in your build log: ML03.ipynb with the prediction written first, the result 50.0, and a sentence on division by zero.

Then lab F01, Numbers, names and predicting Python output.


## Week 2. Python you need (badge: Python You Need)

Product of the week: A flower rule, a loop and a checked function, plus F02.

### Session 4. Decisions and a hand-written flower rule

Question: How often does a three-line rule name the right flower?

Where this is used: Apps decide with rules such as: if the balance is too low, refuse the payment. Botanists also tell flowers apart by measuring petals, and today you write a three-line rule that does it. Can your rule beat a guess?

By the end: you can write an if, elif and else decision, test it at its boundary, and count how often a simple rule is right.

Words: comparison, Boolean, if, else, elif, indentation.

Saved in your build log: ML04.ipynb with the ticket decision tested at three budgets and the flower count 7 out of 8.

### Session 5. Lists, dictionaries and loops

Question: How do I repeat one calculation for every item in a list?

Where this is used: A football league table is a list of teams with points, and a program loops over it to add up every match. Your mobile money statement works the same way. What would you loop over in your favourite sport?

By the end: you can read a list position and a dictionary key, and trace a loop that adds up values.

Words: list, index, dictionary, key, loop, item.

Saved in your build log: ML05.ipynb with the three loop outputs, the stock 8, and the count 2.

### Session 6. Functions and checks that fail loudly

Question: How do I turn my flower rule into a reusable tool and test it?

Where this is used: A fee calculator is a function: write it once and use it for every payment. Software teams also write checks with known answers, so a mistake shows up before a customer finds it. What check would you write for a fee calculator?

By the end: you can write a function that returns a result, and check it against known answers with assert.

Words: function, parameter, argument, return, assert, check.

Saved in your build log: ML06.ipynb with double defined, three passing asserts, and a clean run from the top.

Then lab F02, Lists, vectors and NumPy arrays.


## Week 3. Tables and statistics (badge: Data Detective)

Product of the week: A described table, a revenue column and summary numbers, plus F03.

### Session 7. Tables and reading a CSV file

Question: How many sales are in the practice shop file, and what does each one record?

Where this is used: A shop till, a clinic register and a school timetable are all tables with rows and columns. Programs read such tables from files before they can learn anything. Which table in your life would you like to open in Python?

By the end: you can read a CSV file into a pandas table and say how many rows and columns it has.

New library: pandas.

Words: row and column, header, CSV file, library and import, DataFrame, shape.

Saved in your build log: ML07.ipynb with the first rows, the shape (120, 4), and two sentences on a row and the unit.

### Session 8. Select, filter and calculate new columns

Question: Which item earned the most money in the practice shop?

Where this is used: A shopkeeper asks which item earned the most this week. Answering needs a filter and a new column: units times price. What would you ask of the sales of your own shop?

By the end: you can pick a column, keep rows that meet a condition, add a revenue column and total it by item.

New library: pandas.

Words: select a column, filter, new column, sum, group, revenue.

Saved in your build log: ML08.ipynb with 42 rows, total 247, mean about 5.88, and a sentence on the difference.

### Session 9. Mean, median, range and proportions

Question: What is a typical number of units in a sale, and how spread out are the sales?

Where this is used: News reports quote the average income or the share of people who did something. One very large value can drag the mean up, while the median stays calm. Which would you quote for what most boda-boda rides on your road cost?

By the end: you can calculate the mean, median, range and a proportion, and say which one an extreme value moves most.

New library: numpy.

Words: mean, median, range, percentile, proportion, outlier.

Saved in your build log: ML09.ipynb with mean, median and range for [10, 12, 14, 16] before and after adding 100, and the two rates.

Then lab F03, Variation, proportions and probability.


## Week 4. Clean, chart, question (badge: Clean and Chart)

Product of the week: Your first chart and a project question, plus F04.

### Session 10. Cleaning without hiding evidence

Question: What is wrong with this table, and what did I change?

Where this is used: Clinics, schools and banks collect data typed by busy people, so duplicates and blanks are normal. Data scientists clean the table and write down every change they make. What would you check first in a messy register?

By the end: you can count missing values and duplicates, remove an exact duplicate on a copy, and save a cleaning log.

New library: pandas.

Words: missing value, duplicate, raw data, cleaning log, to_csv, index=False.

Saved in your build log: ML10.ipynb with the counts 2 missing, 1 duplicate, the saved log, and the explanation about zero.

### Session 11. Charts that show what the numbers say

Question: How do I show which item earns most, and how sales vary, in a picture?

Where this is used: Weather forecasts, football stats and mobile money summaries all use charts so people can see a pattern fast. A good chart makes one clear point. What is the one point you want your chart to make?

By the end: you can draw a labelled bar chart, a histogram and a box plot, and write one finding and one limitation.

New library: matplotlib, seaborn.

Words: bar chart, histogram, box plot, axis label, title, finding.

Saved in your build log: ML11.ipynb with a labelled bar chart, one finding with a number, one limitation, and the rainfall answer.

### Session 12. Show your first chart and choose your project question

Question: Can I take a table from a file to a labelled chart and a careful finding on my own?

Where this is used: Every data job starts with one clear question and a table. A coffee trader, a football analyst and a clinic manager each begin that way. Which question would you like your own project to answer?

By the end: you can load a table, check it, total it, chart it, write two findings and a limitation, and ask one prediction question a table could answer.

Words: show-and-tell, reproducible, data dictionary, target, input, limitation.

Saved in your build log: ML12.ipynb: totals, one labelled chart, two findings, one limitation, a missing-value check, a restarted-kernel run, and a three-sentence project question.

Then lab F04, Matrices, weighted sums and slope.


## Week 5. Baselines and a line (badge: Baseline Breaker)

Product of the week: A baseline and a fitted line with their errors compared.

### Session 13. Features, targets and an honest baseline

Question: What did the session 1 model learn from, and how well would a plain guess do?

Where this is used: Banks and mobile lenders use models to flag unusual payments, and they first ask whether the model beats a plain rule. That plain rule is the baseline. What plain guess would you make for tomorrow's weather?

By the end: you can name the features and the target in a table, and calculate a baseline error that any model must beat.

New library: sklearn.

Words: feature, training data, test data, leakage, baseline.

Saved in your build log: ML13.ipynb with baseline 4000.0, error 1000.0, and one named leaked feature.

### Session 14. Predicting a number with a line

Question: How close does a straight line get to the rents of eight homes?

Where this is used: Rents, fares and crop prices often rise in a steady way with size, distance or season, and a straight line is the simplest model of that. Ride-hailing apps show a fare estimate before the trip starts. How far can one line take you?

By the end: you can guess a line by hand, measure its error, and compare it with the line scikit-learn fits.

New library: sklearn.

Words: regression, slope, intercept, fit, predict, error.

Saved in your build log: ML14.ipynb with the prediction 350, the four definitions in the student's own words, and the reason 1000 is risky.

### Session 15. A complete regression experiment

Question: Does the rent model beat a plain guess on homes it has never seen?

Where this is used: A model can look perfect on the homes it learned from and still fail on a new one. Teams that build tools for lending, fares or weather test on cases kept aside. Would you trust a model that was only tested on its own homework?

By the end: you can split data, fit a model and a baseline on the training part, and compare their errors on held-out homes.

New library: sklearn.

Words: train and test split, held-out records, test_size, random_state, baseline model, mean absolute error.

Saved in your build log: ML15.ipynb with both errors, the sentence that the model beats the baseline on held-out homes, and the split unchanged.


## Week 6. Trees and fair comparisons (badge: Fair Judge)

Product of the week: A tree compared fairly with the plain guess on held-back data.

### Session 16. Predicting a category with a decision tree

Question: Does a tree that learned its questions beat my hand-written flower rule?

Where this is used: Doctors and farm advisers sort cases into groups by asking questions in order: is there a fever, are the leaves spotted? A decision tree learns which questions to ask. Can your tree out-guess your own rule?

By the end: you can train a small decision tree on iris, read its first question, and compare its accuracy with a baseline and with the hand rule from session 4.

New library: sklearn.

Words: classification, decision tree, class label, accuracy, majority baseline, depth.

Saved in your build log: ML16.ipynb with both accuracies as percentages, the target and one input named, and the sentence about codes.

### Session 17. Mistakes, overfitting and fair comparisons

Question: When is a very high score a warning sign?

Where this is used: A fraud alert that blocks a real payment upsets a customer, and one that misses fraud costs money. Teams count both kinds of mistake. When would a very high score make you suspicious?

By the end: you can read a confusion matrix, spot an overfitted tree from its training and test scores, and explain why the held-back set must stay untouched until the end.

New library: sklearn, matplotlib.

Words: overfitting, confusion matrix, actual and predicted, validation records, held-back set, peeking.

Saved in your build log: ML17.ipynb with the labelled matrix, 3 right and 2 wrong, and the explanation about tuning on the test.

### Session 18. A fair comparison: does your model beat the plain guess?

Question: Which tree depth is better, and does it beat the plain guess on the held-back flowers?

Where this is used: A football coach tests two formations on matches the team has not practised for. You do the same with two tree depths. Would you pick a formation after one lucky match?

By the end: you can split data into training, validation and held-back parts, choose a model on validation only, and report one held-back result with its limits.

New library: sklearn.

Words: stratify, validation score, frozen choice, split sizes.

Saved in your build log: ML18.ipynb: split sizes 90, 30 and 30, baseline, two validation scores, the chosen depth, one held-back accuracy, a confusion matrix and two limitations.


## Week 7. Your project (badge: Project Builder)

Product of the week: An approved plan, a baseline and a compared model.

### Session 19. Project data and a safe plan

Question: Which dataset and which question can I answer with a fair comparison in two weeks?

Where this is used: Real projects start with a written plan: the question, the data, and the column that would give the answer away. Data teams also protect private information. Which question could your data answer fairly?

By the end: you can describe a supplied dataset, spot a leakage column, and write a seven-heading project plan the instructor can approve.

New library: pandas.

Words: project plan, leakage column, inputs, limits.

Saved in your build log: PROJECT_PLAN.md with seven headings, one named leakage column, and the instructor's approval.

### Session 20. Build the project baseline

Question: How much does a plain guess miss by, before any model helps?

Where this is used: A trader guessing next week's maize price might simply repeat this week's price. A model has to do better than that plain guess to be useful. What is the plain guess for your project?

By the end: you can split data into training, validation and held-back parts, fit a baseline on training only, and draw one descriptive chart.

New library: sklearn, seaborn.

Words: three-way split, baseline error, scatter plot, training only, protected rows.

Saved in your build log: project.ipynb with the split, the baseline error on validation, one labelled chart, a data dictionary and a cleaning log.

### Session 21. Compare, explain and critique

Question: Does my model beat the baseline fairly, and can I defend each input?

Where this is used: When a model helps decide something about people, such as a loan, others ask why. The team must explain which inputs it used and defend them. Can you defend every input in your model?

By the end: you can compare candidate models on the same validation rows, explain why one input is excluded, and check a coding assistant's advice with tests.

New library: sklearn.

Words: fair comparison, candidate model, validation error, coding assistant, AI use log.

Saved in your build log: project.ipynb with the baseline error, one candidate model and its validation error, a written decision, and AI_USE_LOG.md.


## Week 8. Hand over (badge: Showcase)

Product of the week: The final run, the report and the parent showcase.

### Session 22. The final run: your project, ready to share

Question: How well does my frozen model do on rows nobody has used?

Where this is used: Before a model goes live, a team freezes it, tests it once on untouched data and packs the work so someone else can rerun it. Today you do the same. Could a stranger rerun your project tomorrow?

By the end: you can run the held-back check once, report it separately from validation, and share a project that reruns from a restarted kernel.

New library: sklearn.

Words: held-back run, frozen model, handover, restart and run all, limit.

Saved in your build log: A complete local project folder and a clean rerun from a restarted kernel, with the held-back result reported once.

### Session 23. Explain the project to a parent

Question: Can a parent say what my model predicts, how I tested it and why it is limited?

Where this is used: Part of every data job is explaining results to people who do not code, such as managers, farmers or clinic staff. Can you explain your model to a parent in words a ten-year-old would follow?

By the end: you can explain your project in five minutes with five slides, one demonstration, one chart and one limit, without jargon.

Words: claim, demonstration, audience, backup, disclosure.

Saved in your build log: Five slides saved as showcase.pptx, a PDF or screenshot backup, and a timed rehearsal with feedback.

### Session 24. Parent showcase and next steps

Question: Can I show my project and explain how I built it?

Where this is used: Start-ups and tech hubs hold demo days where builders show what they made in a few minutes and answer questions. Today is your demo day. What do you want your family to remember?

By the end: you can present your project, explain one decision, try one small change live with no AI assistant open, and name your next learning goal.

Words: showcase, live change, certificate, project folder, next step, feedback.

Saved in your build log: A showcase talk, one small live change, one strength and one next step, and a certificate decision based on attendance, build log and finished project.
