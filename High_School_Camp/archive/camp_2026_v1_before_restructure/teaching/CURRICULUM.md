# Holiday Data and AI Camp curriculum

Eight weeks, three core classes per week, 24 core sessions per chosen track. ML also includes four foundation labs on a fourth day in weeks 1–4; see FOUNDATION_LABS.md for the required sequence. Audience: S.4–S.6 students and vacists. No programming, spreadsheet or statistics experience assumed.

The proposed session length is three hours, including a 15-minute break. Four proposed two-hour foundation labs bring ML to 80 scheduled hours including breaks; DA has 72. Confirm durations before advertising hour totals. A December 2026 start normally runs into January 2027; map 24 core class dates plus four ML lab dates around holidays before taking payment.


## Machine Learning

### Week 1 session 1 Files and your first instruction

A file stores work; a folder groups files. Python is a language for giving a computer instructions. A notebook combines text cells, which explain, and code cells, which run. Output is what an instruction produces. Text must sit between matching quotation marks. A number such as 3 represents an amount; text such as "3" is a character. print is a ready-made instruction that displays a value; parentheses contain what to display. Read AI_USE_POLICY.md with the instructor. Weeks 1–6 core work is completed without AI-generated solutions.

Practice and evidence: Run the two lines. In a new code cell display your chosen nickname and the result of 7 + 4. Save as ML01.ipynb, close it and reopen it.

### Week 1 session 2 Values names and data types

A value is a piece of information. An integer is a whole number; a float is a decimal; a string is text; a Boolean is True or False. A variable is a name referring to a value. In Python = assigns a value; it does not ask whether two values match. The right side is evaluated before the name on the left is updated. Names have no spaces and Python distinguishes upper and lower case. type(value) reports the type of a value; the word inside parentheses is its input.

Practice and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence explaining why "2500.5" is different.

### Week 1 session 3 Arithmetic input and useful errors

+ adds, - subtracts, * multiplies and / divides. Parentheses group calculations. input displays a prompt and returns text; float converts valid numerical text to a decimal. A comment starts with # and is for people. An error is feedback about an instruction, not a judgement about you. Read the final line of the error first and find the named line.

Practice and evidence: Convert "12.5" to a number and calculate the price of four items. Predict the result before running. Explain why division by zero cannot be used.

### Week 2 session 4 Decisions and true or false

A comparison asks a question and gives True or False. == asks whether values are equal; >= means at least. if runs its indented block only when the question is true; else runs the alternative. A colon starts each block and four spaces show which instructions belong to it. and requires both conditions; or requires at least one.

Practice and evidence: Write a decision for a ticket costing 5000: print "Buy" if budget is at least 5000, otherwise "Save". Test 4999, 5000 and 5001.

### Week 2 session 5 Lists dictionaries and repetition

A list stores several values in order, inside square brackets. Position 0 is the first item. A dictionary stores named pairs inside braces; a key such as "price" lets us retrieve its value. A for loop repeats the indented instructions for each item. The variable after for temporarily names the current item. len counts list items. Square brackets after a list retrieve a position; after a dictionary they retrieve a key. A colon separates each dictionary key from its value.

Practice and evidence: Make a list [2, 4, 6]. Print each value plus 1 using a loop. Make a dictionary with keys name and stock; print the stock. Explain position 0.

### Week 2 session 6 Reusable functions and a first check

A function names a reusable sequence of instructions. def starts its definition. A parameter is the local name for an input; an argument is the value passed when calling it. return sends a result back to the caller. print only displays it. A check compares what happened with what should happen. assert stops with an error if its comparison is false.

Practice and evidence: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2). Save the notebook and run all cells from the start.

### Week 3 session 7 Tables files and importing a library

A table has rows (records) and columns (attributes). A header names a column; a unit states what its numbers mean. CSV means comma-separated values, a plain-text table format. A library is reusable code; import loads it. pandas is a table library; pd is its short name here. A DataFrame is its table object. A path tells Python where a file is. We first build a tiny table to make the structure visible. A dot accesses a named property or operation of an object: sales.shape reports row and column counts; head() shows the first rows. An operation called on an object is a method. to_csv writes a CSV; read_csv reads one. index=False tells pandas not to save its extra row labels. A word followed by = inside a call supplies a named option. Empty parentheses mean no arguments are supplied.

Practice and evidence: Create a two-row table with columns item and price_ugx. Save it to prices.csv and read it back. Write the unit in the column name.

### Week 3 session 8 Selecting filtering and summaries

Selecting a column uses its exact name in square brackets. A filter keeps rows whose comparison is True. groupby gathers rows with the same label before an operation such as sum. A sum adds values; a mean adds values and divides by their count. Distinguish units sold from money earned. sum() adds the selected numbers; mean() averages them. The comparison produces one true/false value per row; the outer brackets keep the true rows. Assigning a new column name creates a calculated column: sales["double_units"] = sales["units"] * 2 doubles each row. Multiplying two numerical columns instead multiplies corresponding rows. This is how units times unit price becomes revenue.

Practice and evidence: Using the same table, keep rows with units >= 3. Calculate the total units and the mean units per row. Explain why these are different quantities.

### Week 3 session 9 Mean median and describing variation

The mean shares a total equally. The median is the middle of sorted values; with an even count it is the mean of the two middle values. The range is largest minus smallest. A large extreme value can move the mean more than the median. A sample is the records observed; it need not represent everyone. These ideas are taught here even if you have seen them in mathematics. statistics.mean and statistics.median are ready-made functions in the imported statistics library. max and min return the largest and smallest list values. Adding two lists with + joins their items; it does not add corresponding items.

Practice and evidence: Calculate mean, median and range for [10, 12, 14, 16]. Add 100 and recalculate. Which summary changes most? Explain using the numbers.

### Week 4 session 10 Cleaning without hiding evidence

A missing value means no recorded value; it is not automatically zero. A duplicate repeats a record, but two equal purchases can be real separate records. A data type describes how a column is stored. Keep raw data unchanged and record each cleaning decision. In this controlled exercise only, an exact duplicate is known to be accidental. None represents a missing entry in this example. isna() marks missing cells as True and others as False; summing those Boolean values counts the missing cells. drop_duplicates() removes identical rows; copy() makes a separate table to work on. pandas mean ignores missing entries here, so state that it describes observed prices only.

Practice and evidence: Write a cleaning log: four raw rows, one removed duplicate, one remaining missing price. Explain why replacing the missing price with zero would change the meaning.

### Week 4 session 11 Charts and cautious findings

A bar chart compares categories; a line chart shows ordered change; a histogram shows the distribution of one numerical variable; a scatter plot compares two numerical variables. Axes name quantities and units. A relationship does not prove one thing causes the other. Start a bar value axis at zero to avoid exaggerating differences. pyplot is the chart interface inside matplotlib; plt is its short name. bar takes categories and heights. ylabel and title add labels; ylim(bottom=0) sets the bottom of the value axis; show displays the figure. A grouped pandas result has index labels and values: totals.index contains category names and totals.values contains the numbers. Pass them to plt.bar(totals.index, totals.values) to chart a grouped table.

Practice and evidence: Make the same chart for [6, 9, 4]. Write one numerical finding and one limitation. Select an appropriate chart for daily rainfall and explain why.

### Week 4 session 12 Checkpoint one and project question

An investigation begins with a question a table can answer. A data dictionary explains column names, units and allowed values. Evidence is a number or chart supporting a claim. Use the supplied camp_shop.csv, not information about classmates. Propose one small prediction question for the final ML project; the supplied synthetic homes or bundled flowers are the approved starting choices. A target is the value you want to predict, such as monthly rent; inputs are the measurements available before predicting it. Here state the question only: model building starts next week.

Practice and evidence: Submit ML12.ipynb with row count, revenue totals, one chart, two findings and one limitation. Add a three-sentence project proposal: question, supplied dataset, target to predict.

### Week 5 session 13 Examples targets and an honest baseline

A feature is an input available when making a prediction. A target is the value we want to predict. Training data teaches the pattern. Validation data helps choose a model. Test data is held aside for a final check. Leakage uses information unavailable at prediction time. A baseline is a simple rule to beat, such as always predicting the training mean. Never calculate a baseline using test answers. sum adds list values and len counts them. abs gives a number's distance from zero. One quarter is 1/4 = 0.25 = 25%; a proportion becomes a percentage when multiplied by 100.

Practice and evidence: For training values [2000, 4000, 6000], predict one new value using the mean baseline. If its actual value is 5000, compute absolute error. Name a leaked feature when predicting a selling price.

### Week 5 session 14 Predicting a number with a line

Regression predicts a number. A straight line uses prediction = slope * input + intercept. Slope describes change per input unit; intercept is the value at input zero, which may be outside realistic use. scikit-learn is a model library. fit learns from examples; predict uses the learned rule on inputs. Double brackets keep a table-shaped input. This exact toy relationship is a syntax demonstration, not evidence of real-world accuracy. A class such as LinearRegression is a model recipe; calling it with parentheses creates a model object. A nested list has one inner list per row. from a_library import a_name loads the named tool.

Practice and evidence: Predict at input 35. Explain the meaning of X, y, fit and predict in your own words. Why is predicting at 1000 risky?

### Week 5 session 15 A complete regression experiment

train_test_split separates records reproducibly; random_state is a fixed random seed for repeating the same split. test_size is the fraction reserved for testing. Mean absolute error (MAE) averages absolute prediction errors and has the target unit. A smaller MAE is better on the same held-out records. We use a supplied synthetic home table only to learn the workflow, not to quote real rents. Four names on the left receive the four outputs of the split in order: training inputs, test inputs, training targets, test targets. DummyRegressor is a baseline model; strategy="mean" predicts the training-target mean. Chaining fit after the constructor creates and trains that model. random_state is for repeatability, not a quality score.

Practice and evidence: Run the example and record the two MAEs. Explain whether the model beats the baseline on these held-out records. Keep the split unchanged; do not keep changing seeds to obtain a better score.

### Week 6 session 16 Predicting a category with a tree

Classification predicts a category. A decision tree asks a sequence of feature questions. A class label names an outcome; it is not a numerical amount even if encoded as 0, 1 or 2. The bundled iris dataset contains flower measurements and species labels, with no downloads required once scikit-learn is installed. Accuracy is correct predictions divided by all predictions. A majority-class baseline always chooses the most frequent training label. load_iris() returns a dataset object. data.data holds the input table; data.target holds the category codes. stratify=data.target preserves approximate class proportions when dividing records. max_depth=2 permits at most two question levels; random_state fixes randomness for repeatability. accuracy_score compares actual labels with predicted labels.

Practice and evidence: Convert both accuracy proportions to percentages. Name the target and one input. Explain why species code 2 does not mean twice species code 1.

### Week 6 session 17 Mistakes overfitting and fair comparisons

Overfitting means learning peculiarities of training examples that do not generalise. A confusion matrix counts actual categories against predicted categories; say aloud which axis is actual. Model choice uses training and validation records. A final test remains untouched until the choice is fixed. Do not promise perfection from a small test. Errors may differ across subgroups even when a total score looks good. labels=[0,1] fixes the displayed row and column order in this two-class example. The final test must stay separate from any choices made after examining validation errors.

Practice and evidence: Draw the 2 by 2 matrix and label both axes. Count correct and incorrect predictions. Explain why trying many settings against final test answers weakens the test.

### Week 6 session 18 Checkpoint two with a locked test

A reproducible experiment can be rerun from the same saved data and instructions. For this checkpoint use iris: hold out 20% as the final test, then reserve 25% of the remaining 80% for validation. This gives about 60% training, 20% validation, 20% final test. Compare tree depth 1 and depth 3 on validation only; freeze the choice before the final test.

Practice and evidence: Submit ML18.ipynb: split sizes, baseline, two validation scores, chosen depth, final test accuracy, confusion matrix, and two limitations. Explain your decision without claiming the highest score proves universal superiority.

### Week 7 session 19 Project data and a safe plan

A project plan fixes a question, dataset, target, inputs, baseline, evaluation method and limits. Use synthetic_homes.csv for regression or bundled iris for classification. Pick the route you can explain. Each learner produces individual evidence, even when discussing ideas with the group. Real personal or school records are outside this beginner project. Review AI_USE_POLICY.md before project work: limited supervised assistance may be demonstrated only after an independent attempt; record any permitted use in AI_USE_LOG.md.

Practice and evidence: Write PROJECT_PLAN.md using those seven headings. Identify one potential leakage column and exclude it. Ask the instructor to approve scope before building.

### Week 7 session 20 Build the project baseline

Keep raw data unchanged. A baseline is useful even if it performs poorly: it tells us whether the complicated approach adds anything. Put decisions and units in text cells next to calculations. Work from a fresh notebook in the project folder.

Practice and evidence: Complete baseline and one descriptive chart. Submit the notebook, data dictionary and cleaning log. If no cleaning was needed, record the checks rather than inventing changes.

### Week 7 session 21 Build compare and explain a model

A model comparison is fair when the records and metric stay the same. Use the taught linear regression for numerical targets or a small decision tree for categories. Prefer a clear explanation over adding algorithms. Keep the final test closed while comparing choices. After the instructor checks readiness, use AI_CODING_ASSISTANTS_LAB.md for 20 minutes of the existing practice block. Critique hints and debugging advice on a separate practice function; keep core project reasoning your own.

Practice and evidence: Add model code, validation score and a short decision to project.ipynb. Ask a partner to identify the target and baseline from your notebook without help.

### Week 8 session 22 Final test and reproducible handover

Freeze the model choice before the final test. Run the final test once for the submitted report. A reproducible handover includes data origin, code, environment instructions and limits. A model on teaching data is a demonstration, not a product ready to make decisions about people.

Practice and evidence: Use the project checklist. Reopen submitted files. Submit project.ipynb, your data dictionary and report.pdf or report.docx together; use the instructor-issued collection route.

### Week 8 session 23 Explain the project to a parent

A presentation is a short explanation for a listener, not a list of library names. A claim needs a visible result and a limitation. Five minutes is enough for one question, one demonstration and one chart. Show only approved, non-personal data; publishing online is optional. After the project rehearsal, the instructor may use MODERN_AI_ORIENTATION.md for a 20-minute introduction connecting these foundations to modern AI. This replaces an optional second rehearsal; it adds no assignment or class.

Practice and evidence: Practise defining prediction, feature and target without jargon. Prepare a screenshot backup for the demonstration and disclose where AI assistance was used.

### Week 8 session 24 Parent showcase and next steps

Demonstrating learning means showing your own work and explaining a decision. The certificate records the completed track and assessed evidence under the published completion policy. It is issued by the programme provider; it is not a university qualification or an external vendor certification.

Practice and evidence: Present your project, acknowledge help, and choose one next learning goal. Keep your project folder and feedback after camp. Demonstrate and explain your work without AI assistance. Close assistant windows and disable generative suggestions; answer an instructor-chosen code question unaided.


## Data Analysis

### Week 1 session 1 Files and your first instruction

A file stores work; a folder groups files. Python is a language for giving a computer instructions. A notebook combines text cells, which explain, and code cells, which run. Output is what an instruction produces. Text must sit between matching quotation marks. A number such as 3 represents an amount; text such as "3" is a character. print is a ready-made instruction that displays a value; parentheses contain what to display. Read AI_USE_POLICY.md with the instructor. Weeks 1–6 core work is completed without AI-generated solutions.

Practice and evidence: Run the two lines. In a new code cell display your chosen nickname and the result of 7 + 4. Save as DA01.ipynb, close it and reopen it.

### Week 1 session 2 Values names and data types

A value is a piece of information. An integer is a whole number; a float is a decimal; a string is text; a Boolean is True or False. A variable is a name referring to a value. In Python = assigns a value; it does not ask whether two values match. The right side is evaluated before the name on the left is updated. Names have no spaces and Python distinguishes upper and lower case. type(value) reports the type of a value; the word inside parentheses is its input.

Practice and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence explaining why "2500.5" is different.

### Week 1 session 3 Arithmetic input and useful errors

+ adds, - subtracts, * multiplies and / divides. Parentheses group calculations. input displays a prompt and returns text; float converts valid numerical text to a decimal. A comment starts with # and is for people. An error is feedback about an instruction, not a judgement about you. Read the final line of the error first and find the named line.

Practice and evidence: Convert "12.5" to a number and calculate the price of four items. Predict the result before running. Explain why division by zero cannot be used.

### Week 2 session 4 Decisions and true or false

A comparison asks a question and gives True or False. == asks whether values are equal; >= means at least. if runs its indented block only when the question is true; else runs the alternative. A colon starts each block and four spaces show which instructions belong to it. and requires both conditions; or requires at least one.

Practice and evidence: Write a decision for a ticket costing 5000: print "Buy" if budget is at least 5000, otherwise "Save". Test 4999, 5000 and 5001.

### Week 2 session 5 Lists dictionaries and repetition

A list stores several values in order, inside square brackets. Position 0 is the first item. A dictionary stores named pairs inside braces; a key such as "price" lets us retrieve its value. A for loop repeats the indented instructions for each item. The variable after for temporarily names the current item. len counts list items. Square brackets after a list retrieve a position; after a dictionary they retrieve a key. A colon separates each dictionary key from its value.

Practice and evidence: Make a list [2, 4, 6]. Print each value plus 1 using a loop. Make a dictionary with keys name and stock; print the stock. Explain position 0.

### Week 2 session 6 Reusable functions and a first check

A function names a reusable sequence of instructions. def starts its definition. A parameter is the local name for an input; an argument is the value passed when calling it. return sends a result back to the caller. print only displays it. A check compares what happened with what should happen. assert stops with an error if its comparison is false.

Practice and evidence: Define double(number) so it returns twice its input. Check double(4), double(0) and double(-2). Save the notebook and run all cells from the start.

### Week 3 session 7 Tables files and importing a library

A table has rows (records) and columns (attributes). A header names a column; a unit states what its numbers mean. CSV means comma-separated values, a plain-text table format. A library is reusable code; import loads it. pandas is a table library; pd is its short name here. A DataFrame is its table object. A path tells Python where a file is. We first build a tiny table to make the structure visible. A dot accesses a named property or operation of an object: sales.shape reports row and column counts; head() shows the first rows. An operation called on an object is a method. to_csv writes a CSV; read_csv reads one. index=False tells pandas not to save its extra row labels. A word followed by = inside a call supplies a named option. Empty parentheses mean no arguments are supplied.

Practice and evidence: Create a two-row table with columns item and price_ugx. Save it to prices.csv and read it back. Write the unit in the column name.

### Week 3 session 8 Selecting filtering and summaries

Selecting a column uses its exact name in square brackets. A filter keeps rows whose comparison is True. groupby gathers rows with the same label before an operation such as sum. A sum adds values; a mean adds values and divides by their count. Distinguish units sold from money earned. sum() adds the selected numbers; mean() averages them. The comparison produces one true/false value per row; the outer brackets keep the true rows. Assigning a new column name creates a calculated column: sales["double_units"] = sales["units"] * 2 doubles each row. Multiplying two numerical columns instead multiplies corresponding rows. This is how units times unit price becomes revenue.

Practice and evidence: Using the same table, keep rows with units >= 3. Calculate the total units and the mean units per row. Explain why these are different quantities.

### Week 3 session 9 Mean median and describing variation

The mean shares a total equally. The median is the middle of sorted values; with an even count it is the mean of the two middle values. The range is largest minus smallest. A large extreme value can move the mean more than the median. A sample is the records observed; it need not represent everyone. These ideas are taught here even if you have seen them in mathematics. statistics.mean and statistics.median are ready-made functions in the imported statistics library. max and min return the largest and smallest list values. Adding two lists with + joins their items; it does not add corresponding items. A proportion is a part divided by a whole; multiply by 100 to express a percentage. For 12 successes in 20 attempts, 12 / 20 * 100 is 60%. Always name the denominator before comparing rates.

Practice and evidence: Calculate mean, median and range for [10, 12, 14, 16]. Add 100 and recalculate. Which summary changes most? Explain using the numbers. Compare 12 successes out of 20 with 15 out of 50. Calculate each percentage and explain why the larger count need not mean the better rate.

### Week 4 session 10 Cleaning without hiding evidence

A missing value means no recorded value; it is not automatically zero. A duplicate repeats a record, but two equal purchases can be real separate records. A data type describes how a column is stored. Keep raw data unchanged and record each cleaning decision. In this controlled exercise only, an exact duplicate is known to be accidental. None represents a missing entry in this example. isna() marks missing cells as True and others as False; summing those Boolean values counts the missing cells. drop_duplicates() removes identical rows; copy() makes a separate table to work on. pandas mean ignores missing entries here, so state that it describes observed prices only.

Practice and evidence: Write a cleaning log: four raw rows, one removed duplicate, one remaining missing price. Explain why replacing the missing price with zero would change the meaning.

### Week 4 session 11 Charts and cautious findings

A bar chart compares categories; a line chart shows ordered change; a histogram shows the distribution of one numerical variable; a scatter plot compares two numerical variables. Axes name quantities and units. A relationship does not prove one thing causes the other. Start a bar value axis at zero to avoid exaggerating differences. pyplot is the chart interface inside matplotlib; plt is its short name. bar takes categories and heights. ylabel and title add labels; ylim(bottom=0) sets the bottom of the value axis; show displays the figure. A grouped pandas result has index labels and values: totals.index contains category names and totals.values contains the numbers. Pass them to plt.bar(totals.index, totals.values) to chart a grouped table.

Practice and evidence: Make the same chart for [6, 9, 4]. Write one numerical finding and one limitation. Select an appropriate chart for daily rainfall and explain why.

### Week 4 session 12 Checkpoint one with Python and pandas

This checkpoint combines the Python, pandas, statistics, cleaning and plotting skills already practised. Use camp_shop.csv. A revenue column multiplies the units and price in each row: sales["revenue_ugx"] = sales["units"] * sales["unit_price_ugx"]. Selecting an existing column reads it; assigning a new column name creates it. Revenue is money from sales, not profit: costs are absent. Keep the raw CSV unchanged. sales.shape[0] reads the row count from the shape pair; by_item.index contains product labels and by_item.values contains the totals. A notebook preserves the calculation and explanation together.

Practice and evidence: In DA12.ipynb calculate total units, total revenue and revenue by item. Make one labelled chart and write two findings plus one limitation in text cells. Record missing-value checks and any cleaning actually needed. Run all cells from a restarted kernel, save and submit DA12.ipynb with a short report.pdf or report.docx using the instructor-issued route.

### Week 5 session 13 Databases and your first SQL query

A database stores organised tables. SQL is a language for asking questions of those tables. A query is one such instruction. SELECT names columns and FROM names the table. The semicolon ends the statement. The prepared database is a local SQLite file; no online account is needed.

Practice and evidence: Open camp_shop.sqlite in DB Browser for SQLite. Choose Execute SQL, type the example and run it. Write a query returning sale_id, item and unit_price_ugx.

### Week 5 session 14 SQL filters and ordering

WHERE keeps records meeting a condition. Text literals use single quotes in SQL; numbers do not need quotes. AND requires both conditions. ORDER BY sorts results; DESC means descending. LIMIT reduces the displayed row count. Filtering is not deleting.

Practice and evidence: List Juice records with units at least 4, sorted by units descending then sale_id ascending. Return sale_id, item and units.

### Week 5 session 15 SQL totals and groups

SUM adds values; COUNT(*) counts records. GROUP BY creates a result per category. AS gives a result column a readable name. An expression such as units * unit_price_ugx is calculated for each record before SUM combines it.

Practice and evidence: Calculate total units and number of sales records per item. Name the columns total_units and record_count. Compare with your pandas groupby result.

### Week 6 session 16 Joining two tables carefully

A key identifies a row. A join connects records using matching keys. sales.item matches products.item here; products has exactly one row per item. LEFT JOIN keeps every sale even if product details are missing. A duplicate product key would multiply matching sale rows and overstate totals.

Practice and evidence: Join category to sales, then calculate revenue by category. Compare the grand total before and after the join.

### Week 6 session 17 Nulls validation and repeatable work

NULL means missing or unknown in a database. Test it with IS NULL, not = NULL. Validation checks whether results obey expectations: row counts, allowed values and reconciled totals. Saving a query preserves the calculation; saving only a result does not preserve its method.

Practice and evidence: Write queries counting records, checking missing item names and calculating total revenue. Save queries.sql with a comment before each check.

### Week 6 session 18 Checkpoint two across Python and SQL

Independent methods can catch mistakes: a SQL summary and a pandas summary should agree if they use the same rows and definitions. A discrepancy is a reason to investigate, not to choose whichever number looks better.

Practice and evidence: Submit DA18.sql, results.csv, DA18.ipynb and a short explanation of your row-count, null and total checks. Explain one join-risk example.

### Week 7 session 19 Project question and evidence plan

A final analysis project serves a reader: decide who needs the answer and what decision it could inform. Use the supplied shop data. Define three questions you can answer with taught methods. No forecasting or model training is required in the Data Analysis track. Review AI_USE_POLICY.md before project work: limited supervised assistance may be demonstrated only after an independent attempt; record any permitted use in AI_USE_LOG.md.

Practice and evidence: Write PROJECT_PLAN.md. List the raw file, measures, charts, SQL queries and limitations. Ask the instructor to approve a narrow scope.

### Week 7 session 20 Build a reliable analysis

Reliability means the reader can follow the steps from raw records to your answer. A cleaning log explains changes, including when none were necessary. Make one calculation at a time and compare it with a small hand-worked example.

Practice and evidence: Complete the calculation layer and ask a partner to rerun one SQL query. Save feedback and fix the first unexplained discrepancy.

### Week 7 session 21 Build and test the project chart report

A chart report should answer the project questions without needing a verbal tour. Use few charts, readable labels, units, the covered dates and a visible data-source note. Chart choice should follow the question, not the prettiest template. After the instructor checks readiness, use AI_CODING_ASSISTANTS_LAB.md for 20 minutes of the existing practice block. Critique hints and debugging advice on a separate practice function; keep core project reasoning your own.

Practice and evidence: Give a peer 30 seconds to find the largest category and total. Record where they hesitate and simplify the notebook headings. To include a chart in the report, call plt.savefig("revenue.png", bbox_inches="tight") before plt.show(). savefig writes the image; bbox_inches="tight" includes labels. Insert the saved PNG into the report using Insert > Pictures/Image.

### Week 8 session 22 Write the report and package the evidence

A report connects a question, method, result and recommendation. Separate observed facts from proposals. A complete handover includes the working Python notebook and SQL, not only the polished picture. Restart the kernel and run all cells from top to bottom before saving. Use a text cell for each question, method, finding and limitation. Keep personal information out of all public copies.

Practice and evidence: Submit project.ipynb, queries.sql, cleaning_log.md and report.pdf or report.docx. Include your data dictionary. Check every file opens and the totals agree.

### Week 8 session 23 Rehearse a five minute explanation

A parent should understand the question and the conclusion without knowing SQL. Explain a chart in ordinary language: what is compared, the unit, the biggest difference and the limitation. A demo is evidence that you understand your own work. After the project rehearsal, the instructor may use MODERN_AI_ORIENTATION.md for a 20-minute introduction connecting these foundations to modern AI. This replaces an optional second rehearsal; it adds no assignment or class.

Practice and evidence: Practise answering: where did this number come from, what did you clean, and what cannot this data tell us? Disclose help and AI use.

### Week 8 session 24 Parent showcase and next steps

The showcase is a chance to demonstrate learning, accept questions and celebrate progress. The certificate identifies the Data Analysis track and the evidence completed. It is issued by the programme provider, not Google, IBM or a university.

Practice and evidence: Present your project and name one next skill to practise. Keep the final files and feedback in your own folder. Demonstrate and explain your work without AI assistance. Close assistant windows and disable generative suggestions; answer an instructor-chosen code question unaided.
