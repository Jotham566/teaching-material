# Python for Data Analysis: eight-week plan

Relative plan. Exact dates and holiday breaks are not confirmed. Core sessions propose 180 minutes including a 15-minute break.

Two 45 to 60 minute practice blocks on non-class days are the starting allowance. The repeat-and-change task in each session is part of these blocks, not extra homework. Weeks 1 to 6 portfolios carry the existing 20% weight; checkpoints and the project keep their own weights.

Default clock for every session unless its guide says otherwise: 10 minutes recall: retrieve yesterday, three questions on paper; 50 minutes block a: predict, run, investigate, modify; 15 minutes break away from screens; 50 minutes block b: predict, run, investigate, modify; 40 minutes make: the independent task and the project journal; 15 minutes exit ticket, save, and an individual check with each learner.


## Week 1. Meet the data: sessions 01 to 03

Product of the week: A notebook that reads the shop table and an error log.

Practice between classes: Change two quantities in the revenue calculation, predict the result on paper, run it and explain it.

### DA01. Open a notebook and read your first table

By the end: you can open, run, save and reopen a notebook, and read a table of shop sales into it.

Exercise and evidence: In a new code cell show your nickname and the result of 7 + 4. Then show the first three rows of the shop table with head(3). Save the notebook as DA01.ipynb, close it and open it again.

### DA02. Values, names and types

By the end: you can store numbers and text under names, and say what type each one is.

Exercise and evidence: Create a decimal price of 2500.5 and a quantity of 2. Print the total. Write one sentence on why "2500.5" with quotation marks behaves differently.

### DA03. Arithmetic, revenue and reading errors

By the end: you can calculate revenue for a sale, check it by hand, and read an error message to find the line to fix.

Exercise and evidence: Convert the text "12.5" to a number and calculate the price of four items at that price. Predict the result before you run it. Write one sentence on why division by zero cannot be answered.


## Week 2. Python you need: sessions 04 to 06

Product of the week: Three small Python programs with checks that pass.

Practice between classes: Change a function input, test zero and one ordinary value, and trace a loop over three items.

### DA04. Conditions and decisions

By the end: you can write a decision that gives a different answer for True and False, and test it at the edge.

Exercise and evidence: Write a decision for a ticket that costs 5000. Print "Buy" if the budget is at least 5000 and otherwise print "Save". Test 4999, 5000 and 5001.

### DA05. Lists, dictionaries and loops

By the end: you can store several values in a list, look one up by position, and use a loop to add them up.

Exercise and evidence: Make a list [2, 4, 6]. Print each value plus 1 with a loop. Make a dictionary with the keys name and stock and print the stock. Explain why position 0 is the first.

### DA06. Functions and checks that fail loudly

By the end: you can write a function that returns a result, and use assert to check it on known cases.

Exercise and evidence: Write price_after_discount(price, percent) that returns the price after a percentage discount. Check it with assert for 0 percent, 10 percent and 100 percent on a price of 2000. Save the notebook and run all cells from the top.


## Week 3. Tables in pandas: sessions 07 to 09

Product of the week: Revenue by item and by branch, checked against the hand total.

Practice between classes: Rerun the grouped total on a different column and reconcile it with a hand count of five rows.

### DA07. A table in Python: DataFrame, columns and reading a CSV

By the end: you can build a small table, read a CSV file into one, and say how many rows and columns it has and what each column holds.

Exercise and evidence: Read sunrise_sales.csv, the Sunrise Shops sales. Print its shape and its column names. Write which column holds the date and which holds the price of one unit.

### DA08. Select, filter and calculate a revenue column

By the end: you can pick a column, keep the rows that meet a condition, and add a revenue column.

Exercise and evidence: Keep the Pen sales that have 4 units or more. Count them and add up the revenue they bring in. Say why the count and the revenue are different quantities.

### DA09. Sort, group, mean and median

By the end: you can total a column by group, sort the result, and say when the median describes a column better than the mean.

Exercise and evidence: Add the line_value column and total it for each branch_id in the Sunrise sales. Sort the three totals from largest to smallest. Check that the three totals add up to the overall total.


## Week 4. Clean and chart: sessions 10 to 12

Product of the week: Checkpoint one: a cleaned table, three labelled charts, findings.

Practice between classes: Finish the cleaning log and the labelled charts. Rerun checkpoint one from a restarted kernel.

### DA10. Cleaning without hiding evidence

By the end: you can find missing values and duplicates, remove the duplicates on a copy, and save a cleaning log that says what you did.

Exercise and evidence: Write a cleaning log for the four-row table in Block A: four raw rows, one duplicate removed, one price still missing. Save it as a CSV with to_csv. Write one sentence on why replacing the missing price with zero would change what the data says.

### DA11. Charts that say what the numbers say

By the end: you can draw a bar chart, a line chart, a histogram and a scatter plot with labelled axes, and state one finding and one limit for each.

Exercise and evidence: Chart the Sunrise revenue by branch. Use a dictionary to turn the ids 1, 2 and 3 into the names Central Market, Campus Gate and Roadside. Label the axis, start it at zero and write one finding and one limitation.

### DA12. Checkpoint one: load, summarise, chart and explain

By the end: you can read a table, check it, summarise it, chart it and explain two findings and one limit, from a restarted notebook.

Exercise and evidence: In DA12.ipynb use sunrise_sales.csv. 1) Report the number of rows and the total revenue. 2) Check for missing values and duplicates and report the counts. 3) Total the revenue by branch with names from a dictionary and sort the result. 4) Draw one labelled chart. 5) Write two findings and one limitation in text cells. Restart the kernel, run all cells from the top, save and submit DA12.ipynb with a short report.pdf or report.docx through the route in START_HERE.md.


## Week 5. Explore with NumPy and seaborn: sessions 13 to 15

Product of the week: Spread, distributions and relationships explored, with what each shows.

Practice between classes: Explain one chart and one correlation in your own words, with its limit.

### DA13. NumPy: the numbers underneath pandas

By the end: you can turn a column into a NumPy array, calculate its mean, median, spread and percentiles, and find unusually large values.

Exercise and evidence: Take the revenue_ugx column of the daily summary as a NumPy array. Find its mean, median and the 25th and 75th percentiles with NumPy. Then find the same four numbers with pandas and check that the two routes agree.

### DA14. Exploring distributions with seaborn

By the end: you can draw a histogram and a box plot with seaborn and describe the shape, the middle and the outliers of a column.

Exercise and evidence: Explore the daily customer counts. Draw a histogram of customers_counted and a box plot of customers_counted for each branch. Write the median for each branch and one finding in a sentence.

### DA15. Exploring relationships: scatter plots, correlation and cause

By the end: you can draw a scatter plot coloured by group, read a correlation number, and say why a correlation does not prove one thing causes another.

Exercise and evidence: Check the rain question for each shop separately. For each branch find the correlation between rain_mm and customers_counted. Say whether rain matters at any shop and why a correlation could not prove that it does.


## Week 6. Messy data and two tables: sessions 16 to 18

Product of the week: Checkpoint two: clean, merge and reconcile, with the residual named.

Practice between classes: Finish checkpoint two. Find the residual difference and name its cause.

### DA16. Cleaning the raw export

By the end: you can turn a messy export into a clean table with a pipeline that reruns, and explain why its total is lower than the true total.

Exercise and evidence: Put the cleaning steps in one function called clean_sales(raw) that returns the clean table and the excluded rows. Run it on the raw export and check with assert that the clean table has 1473 rows and the clean revenue is 6250500. Write one sentence naming the residual and its cause.

### DA17. Merging two tables and the fan-out trap

By the end: you can merge two tables on a key, check the row count before and after, and spot a duplicated key that inflates a total.

Exercise and evidence: Merge the sales with sunrise_branches.csv on branch_id to get the branch names. Check that the row count is unchanged. Total the revenue by branch name and reconcile it with the totals you found in session 9.

### DA18. Checkpoint two: clean, merge and reconcile

By the end: you can clean a raw export, merge it with a lookup table, and report a total together with its named difference from the true total.

Exercise and evidence: In DA18.ipynb start from sunrise_sales_raw.csv. 1) Clean it with a function and report the rows kept, rows excluded and the cleaning steps. 2) Merge the clean table with the products table on product_id. Check that the key is unique and that the row count is unchanged. 3) Total the revenue by category. 4) Compare the cleaned total with the true total in sunrise_sales.csv. Name the residual and its cause. 5) Write two limitations. Run from a restarted kernel, save and submit DA18.ipynb and a short explanation of your checks through the route in START_HERE.md.


## Week 7. Show it: sessions 19 to 21

Product of the week: An approved project plan and a rerunnable notebook.

Practice between classes: Build the approved project incrementally. Save your independent attempt before any supervised AI critique.

### DA19. Project question and a safe plan

By the end: you can write a narrow project plan with a question, the data, the measures, the charts and the limits, and have it approved.

Exercise and evidence: Write PROJECT_PLAN.md with the seven headings. Name the data file and its licence or its invented status. List the three questions, the columns each needs, the charts and the limitations. Ask the instructor to approve a narrow scope before you build.

### DA20. Build a reliable analysis

By the end: you can build the calculations for your project so that each one is checked by hand and by a second route, and a partner can rerun them.

Exercise and evidence: Work from a protected copy of the raw data. Write the cleaning log, including a log that says no change was needed if that is true. Build one calculation at a time. For each, compare with a small hand-worked example and with a second route (pandas against NumPy, or a merged total against an unmerged one). Ask a partner to rerun one calculation from your notebook. Write down the first discrepancy they find and fix it.

### DA21. Build and test the chart report

By the end: you can build a chart report that a stranger reads in 30 seconds, and you can critique a coding assistant's hint with a test.

Exercise and evidence: Build the chart report. Use few charts, readable labels with units, the covered dates and a visible data source note. Write two findings and one limitation next to their evidence. Give a peer 30 seconds to find the largest category and its total, and record where they hesitate. To put a chart in your report, call plt.savefig("revenue.png", bbox_inches="tight") before plt.show(), then insert the PNG with Insert and Pictures. When the instructor confirms you are ready, spend 20 minutes with AI_CODING_ASSISTANTS_LAB.md: critique a hint on the practice function, run a test and log it in AI_USE_LOG.md.


## Week 8. Hand over: sessions 22 to 24

Product of the week: The report, the five-minute talk and the unaided demonstration.

Practice between classes: Rerun and hand in the project at session 22; rehearse an unaided explanation and a small code change.

### DA22. Report and handover

By the end: you can hand over a project that another person can open, rerun and check.

Exercise and evidence: Restart the kernel and run all cells from the top. Confirm every number in the report appears in an output. Write the one-page report: question, data, method, three findings with their values, one recommendation and one limitation. Export it to PDF and reopen it. Submit project.ipynb, cleaning_log.md, your data dictionary, report.pdf or report.docx and AI_USE_LOG.md together through the route in START_HERE.md. Keep personal information out of every file.

### DA23. Explain it to a parent

By the end: you can explain your project to a listener who has never seen code, in five minutes, with a chart and a limit.

Exercise and evidence: Make five slides: my question; what data I used; what I did; my most useful finding with its chart; the limitation and next step. Save as showcase.pptx and keep a PDF and screenshots as a backup. Rehearse with a timer. Practise answering: where did this number come from, what did you clean, and what can this data not tell us. Disclose any help or AI use. Show only invented or approved non-personal data. The instructor may follow the rehearsal with MODERN_AI_ORIENTATION.md, a 20-minute optional introduction with no assignment or mark.

### DA24. Parent showcase and next steps

By the end: you can present your project, answer questions, and change a small part of it live without AI assistance.

Exercise and evidence: Present your project for five minutes and answer three minutes of questions. Explain one calculation, one chart and one limitation. The instructor then chooses one small change, and you make it unaided. Close assistant windows and turn off generative suggestions first. Acknowledge any help you had. Choose one next learning goal. Keep your project folder and feedback.


## Supporting material and delivery gates

Data: see data/DATA_DICTIONARY.md and data/sunrise/DATA_DICTIONARY.md. Policies in handbook/: AI_USE_POLICY.md, ASSESSMENT_AND_SHOWCASE.md, PROJECT_RUBRIC.md. Run programme/preflight_stack.py on every laptop before day one. Pilot a Python foundations session and a pandas session with a beginner first. No school submission platform or automatic end-to-end marking is deployed by this pack.
