# Machine Learning: eight-week plan

Relative plan. Exact dates and holiday breaks are not confirmed. Core sessions propose 180 minutes including a 15-minute break; each ML lab proposes 120 minutes including a 10-minute break. Insert each lab after that week's third core session.

Two 45 to 60 minute practice blocks on non-class days are the starting allowance. The repeat-and-change task in each session is part of these blocks, not extra homework. Weeks 1 to 6 portfolios carry the existing 20% weight; checkpoints and the project keep their own weights.

Default clock for every session unless its guide says otherwise: 10 minutes recall: retrieve yesterday, three questions on paper; 50 minutes block a: predict, run, investigate, modify; 15 minutes break away from screens; 50 minutes block b: predict, run, investigate, modify; 40 minutes make: the independent task and the project journal; 15 minutes exit ticket, save, and an individual check with each learner.


## Week 1. Python and a first prediction: sessions 01 to 03

Product of the week: A first prediction run, a small calculation notebook and F01.

Practice between classes: Change two quantities in the arithmetic example, predict the result on paper, run it and explain it.

Lab: ML03 then F01, Numbers, names and predicting Python output.

### ML01. Your first instruction and your first prediction

By the end: you can run, save and reopen a notebook, and you can say what a prediction is using the rent example.

Exercise and evidence: In a new code cell print your nickname and the result of 7 + 4. In another cell estimate the rent for 80 square metres. Save as ML01.ipynb, close it and reopen it. With the instructor, read AI_USE_POLICY.md: in weeks 1 to 6 all core work is your own, with no AI-generated solutions.

### ML02. Values, names and types

By the end: you can create whole numbers, decimals and text, and predict what happens when a name is given a new value.

Exercise and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence on why "2500.5" with quotation marks is different.

### ML03. Arithmetic, converting text and reading errors

By the end: you can calculate with the five basic operators, turn text into a number, and find the line an error points to.

Exercise and evidence: Convert "12.5" to a number and calculate the price of four items. Predict the answer before you run it. Explain why nobody can divide by zero.


## Week 2. Python you need: sessions 04 to 06

Product of the week: A flower rule, a loop and a checked function, plus F02.

Practice between classes: Change the function inputs, test zero and one ordinary value, and trace a loop over three items.

Lab: ML06 then F02, Lists, vectors and NumPy arrays.

### ML04. Decisions and a hand-written flower rule

By the end: you can write an if, elif and else decision, test it at its boundary, and count how often a simple rule is right.

Exercise and evidence: A ticket costs UGX 5000. Write a decision that prints Buy when the budget is at least 5000 and Save otherwise. Test 4999, 5000 and 5001. Then say how many of the eight flowers your flower rule names correctly.

### ML05. Lists, dictionaries and loops

By the end: you can read a list position and a dictionary key, and trace a loop that adds up values.

Exercise and evidence: Make the list [2, 4, 6] and print each value plus 1 with a loop. Make a dictionary with the keys name and stock and print the stock. Then loop over the eight petal lengths 1.4, 1.4, 4.7, 4.5, 4.9, 6.0, 5.1, 5.9 and count how many are below 2.5.

### ML06. Functions and checks that fail loudly

By the end: you can write a function that returns a result, and check it against known answers with assert.

Exercise and evidence: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2) with assert. Save the notebook and run all cells from the top.


## Week 3. Tables and statistics: sessions 07 to 09

Product of the week: A described table, a revenue column and summary numbers, plus F03.

Practice between classes: Compare mean and median before and after an extreme value. Keep a note on the units.

Lab: ML09 then F03, Variation, proportions and probability.

### ML07. Tables and reading a CSV file

By the end: you can read a CSV file into a pandas table and say how many rows and columns it has.

Exercise and evidence: Read synthetic_homes.csv. Show its first rows and its shape. Say what each row stands for and what unit rent_ugx is in.

### ML08. Select, filter and calculate new columns

By the end: you can pick a column, keep rows that meet a condition, add a revenue column and total it by item.

Exercise and evidence: Keep the rows with units of at least 3. Calculate the total units and the mean units per row. Say why these two numbers are different quantities.

### ML09. Mean, median, range and proportions

By the end: you can calculate the mean, median, range and a proportion, and say which one an extreme value moves most.

Exercise and evidence: Compare 12 successes out of 20 attempts with 15 out of 50. Calculate each percentage and explain why the larger count does not have to mean the better rate.


## Week 4. Clean, chart, question: sessions 10 to 12

Product of the week: Checkpoint one with a chart and a project question, plus F04.

Practice between classes: Finish the cleaning log and labelled charts. Rerun checkpoint one; write two findings and one limitation.

Lab: ML12 then F04, Matrices, weighted sums and slope.

### ML10. Cleaning without hiding evidence

By the end: you can count missing values and duplicates, remove an exact duplicate on a copy, and save a cleaning log.

Exercise and evidence: Write a cleaning log for this table: four raw rows, one removed duplicate and one remaining missing price. Save it as my_log.csv and read it back. Explain why replacing the missing price with 0 would change its meaning.

### ML11. Charts that show what the numbers say

By the end: you can draw a labelled bar chart, a histogram and a box plot, and write one finding and one limitation.

Exercise and evidence: Make the same bar chart for the values 6, 9 and 4 for Book, Pen and Juice. Write one finding with a number and one limitation. Say which chart type you would use for daily rainfall, and why.

### ML12. Checkpoint one and a project question

By the end: you can load a table, check it, total it, chart it, write two findings and a limitation, and ask one prediction question a table could answer.

Exercise and evidence: In ML12.ipynb report the row count, the revenue by item, one chart, two findings and one limitation, and record your missing-value check. Run all cells from a restarted kernel and save. Add your three-sentence project question.


## Week 5. Baselines and a line: sessions 13 to 15

Product of the week: A baseline and a fitted line with their errors compared.

Practice between classes: Explain the baseline and check one prediction error by hand.

### ML13. Features, targets and an honest baseline

By the end: you can name the features and the target in a table, and calculate a baseline error that any model must beat.

Exercise and evidence: For training values [2000, 4000, 6000], find the baseline guess for a new item. If its real value is 5000, calculate the absolute error. Name one leaked feature if you were predicting a selling price.

### ML14. Predicting a number with a line

By the end: you can guess a line by hand, measure its error, and compare it with the line scikit-learn fits.

Exercise and evidence: Use X = [[10], [20], [30], [40]] and y = [100, 200, 300, 400]. Fit a line and predict at 35. Explain in your own words what X, y, fit and predict mean, and why predicting at 1000 is risky.

### ML15. A complete regression experiment

By the end: you can split data, fit a model and a baseline on the training part, and compare their errors on held-out homes.

Exercise and evidence: Run the experiment, record the two errors, and say whether the model beats the baseline on the held-out homes. Keep the split as it is. Do not keep changing random_state to get a better score.


## Week 6. Trees and fair tests: sessions 16 to 18

Product of the week: Checkpoint two: a tree compared fairly with a locked final test.

Practice between classes: Finish checkpoint two. Explain one split or model mistake and repair the method, not the number.

### ML16. Predicting a category with a decision tree

By the end: you can train a small decision tree on iris, read its first question, and compare its accuracy with a baseline and with the hand rule from session 4.

Exercise and evidence: Convert both accuracies to percentages. Name the target and one input. Explain why species code 2 is not twice species code 1.

### ML17. Mistakes, overfitting and fair comparisons

By the end: you can read a confusion matrix, spot an overfitted tree from its training and test scores, and explain why the final test must stay locked.

Exercise and evidence: Draw the 2 by 2 matrix for the toy answers and label both axes. Count the right and the wrong predictions. Explain why trying many settings against the final test answers weakens that test.

### ML18. Checkpoint two with a locked test

By the end: you can split data into training, validation and final test, choose a model on validation only, and report one final test result with its limits.

Exercise and evidence: Submit ML18.ipynb with: the split sizes, the baseline, two validation scores, the chosen depth, the final test accuracy, the confusion matrix and two limitations. Explain your decision without claiming that the highest score proves one depth is best in general.


## Week 7. Your project: sessions 19 to 21

Product of the week: An approved plan, a baseline and a compared model.

Practice between classes: Build the approved project incrementally. Save your independent attempt before any supervised AI critique.

### ML19. Project data and a safe plan

By the end: you can describe a supplied dataset, spot a leakage column, and write a seven-heading project plan the instructor can approve.

Exercise and evidence: Write PROJECT_PLAN.md using the seven headings. Name one leakage column and exclude it. Ask the instructor to approve the scope before you build.

### ML20. Build the project baseline

By the end: you can split data into training, validation and locked test, fit a baseline on training only, and draw one descriptive chart.

Exercise and evidence: Complete the three-way split, the baseline and one labelled chart for your own project dataset. Save the notebook, your data dictionary and the cleaning log. If no cleaning was needed, record the checks that found nothing.

### ML21. Compare, explain and critique

By the end: you can compare candidate models on the same validation rows, explain why one input is excluded, and check a coding assistant's advice with tests.

Exercise and evidence: Add model code, the validation error and a short decision to project.ipynb. Ask a partner to name your target and baseline from the notebook alone. Record any assistance in AI_USE_LOG.md or write No AI assistance used.


## Week 8. Hand over: sessions 22 to 24

Product of the week: The final test, the report and the unaided demonstration.

Practice between classes: Rerun and hand in the project at session 22; rehearse an unaided explanation and a small code change.

### ML22. The final test and a reproducible handover

By the end: you can run the final test once, report it separately from validation, and hand over a project that reruns from a restarted kernel.

Exercise and evidence: Use the project checklist. Reopen all submitted files. Submit project.ipynb, your data dictionary and report.pdf or report.docx together through the instructor's collection route.

### ML23. Explain the project to a parent

By the end: you can explain your project in five minutes with five slides, one demonstration, one chart and one limit, without jargon.

Exercise and evidence: Practise defining prediction, feature and target without jargon. Save a screenshot backup of your demonstration and disclose any AI assistance.

### ML24. Parent showcase and next steps

By the end: you can present your project, explain one decision, make one small code change without AI, and name your next learning goal.

Exercise and evidence: Present your project, say who helped you, and choose one next learning goal. Keep your project folder and feedback after the camp.


## Supporting material and delivery gates

Data: see data/DATA_DICTIONARY.md and data/sunrise/DATA_DICTIONARY.md. Policies in handbook/: AI_USE_POLICY.md, ASSESSMENT_AND_SHOWCASE.md, PROJECT_RUBRIC.md. Run programme/preflight_stack.py on every laptop before day one. Pilot a Python foundations session and a pandas session with a beginner first. No school submission platform or automatic end-to-end marking is deployed by this pack.
