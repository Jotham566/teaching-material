# Python for Data Analysis: curriculum

Eight weeks, three core sessions a week, 24 core sessions, each proposed at three hours including a 15-minute break. Audience: S.4 to S.6 students and school leavers. No programming, spreadsheet or statistics experience is assumed. Confirm session length and dates before advertising hour totals.


## Week 1. Meet the data

Product of the week: A notebook that reads the shop table and an error log.

### Session 1. Open a notebook and read your first table

Question: What does one week of sales in a small shop look like?

By the end: you can open, run, save and reopen a notebook, and read a table of shop sales into it.

New library: pandas.

Words: notebook, cell, run, output, file, table.

Evidence: DA01.ipynb that reopens with the nickname, 11 and three table rows.

### Session 2. Values, names and types

Question: What kind of thing is each part of a sale?

By the end: you can store numbers and text under names, and say what type each one is.

Words: value, integer, float, string, variable, type.

Evidence: DA02.ipynb with the total 5001.0 and a sentence about the quotation marks.

### Session 3. Arithmetic, revenue and reading errors

Question: How much money did the first three sales bring in?

By the end: you can calculate revenue for a sale, check it by hand, and read an error message to find the line to fix.

Words: operator, expression, order of operations, comment, error message, line number.

Evidence: DA03.ipynb with 50.0, the prediction written before the run, and an error log with two errors read correctly.


## Week 2. Python you need

Product of the week: Three small Python programs with checks that pass.

### Session 4. Conditions and decisions

Question: Is this sale big enough to count as a large order?

By the end: you can write a decision that gives a different answer for True and False, and test it at the edge.

Words: comparison, Boolean, if, else, indentation, and, or.

Evidence: DA04.ipynb with the decision tested at 4999, 5000 and 5001.

### Session 5. Lists, dictionaries and loops

Question: How many units did the first six sales sell in total?

By the end: you can store several values in a list, look one up by position, and use a loop to add them up.

Words: list, index, dictionary, key, loop, running total.

Evidence: DA05.ipynb with the loop output 3, 5, 7, the stock 8 and the explanation of position 0.

### Session 6. Functions and checks that fail loudly

Question: Can we trust our revenue calculation on cases we already know the answer to?

By the end: you can write a function that returns a result, and use assert to check it on known cases.

Words: function, parameter, argument, return, assert, edge case.

Evidence: DA06.ipynb with the function and three passing asserts, rerun from the top.


## Week 3. Tables in pandas

Product of the week: Revenue by item and by branch, checked against the hand total.

### Session 7. A table in Python: DataFrame, columns and reading a CSV

Question: What is in each table we have been given?

By the end: you can build a small table, read a CSV file into one, and say how many rows and columns it has and what each column holds.

New library: pandas.

Words: row, column, header, CSV, DataFrame, library.

Evidence: DA07.ipynb with shape (1513, 6), the six column names and two sentences naming the date and price columns.

### Session 8. Select, filter and calculate a revenue column

Question: How much money did the practice shop take in, and where did it come from?

By the end: you can pick a column, keep the rows that meet a condition, and add a revenue column.

Words: select, filter, mask, new column, revenue, sum.

Evidence: DA08.ipynb with 14 sales, 90000 shillings and a sentence on the difference.

### Session 9. Sort, group, mean and median

Question: Which item earns the most, and what is a typical sale in a small practice shop?

By the end: you can total a column by group, sort the result, and say when the median describes a column better than the mean.

Words: group, sort, mean, median, proportion, denominator.

Evidence: DA09.ipynb with three sorted totals that add to 6375900 and a passing assert.


## Week 4. Clean and chart

Product of the week: Checkpoint one: a cleaned table, three labelled charts, findings.

### Session 10. Cleaning without hiding evidence

Question: What is wrong with the raw Sunrise sales file, and how many rows does each problem touch?

By the end: you can find missing values and duplicates, remove the duplicates on a copy, and save a cleaning log that says what you did.

Words: raw data, missing value, duplicate, data type, copy, cleaning log.

Evidence: DA10.ipynb and my_log.csv with the three counts and the sentence about zero.

### Session 11. Charts that say what the numbers say

Question: Which chart shows this comparison most clearly?

By the end: you can draw a bar chart, a line chart, a histogram and a scatter plot with labelled axes, and state one finding and one limit for each.

New library: matplotlib.

Words: matplotlib, bar chart, line chart, histogram, scatter plot, axis label.

Evidence: DA11.ipynb with a labelled bar chart of three branches, one finding and one limitation.

### Session 12. Checkpoint one: load, summarise, chart and explain

Question: What do the Sunrise Shops sales tell us about the three shops?

By the end: you can read a table, check it, summarise it, chart it and explain two findings and one limit, from a restarted notebook.

Evidence: DA12.ipynb that reruns from a restarted kernel, with the rows, total, checks, sorted branch totals, one labelled chart, two findings and one limitation. Marks follow ASSESSMENT_AND_SHOWCASE.md.


## Week 5. Explore with NumPy and seaborn

Product of the week: Spread, distributions and relationships explored, with what each shows.

### Session 13. NumPy: the numbers underneath pandas

Question: How spread out are the daily customer counts, and which sales are unusually large?

By the end: you can turn a column into a NumPy array, calculate its mean, median, spread and percentiles, and find unusually large values.

New library: NumPy.

Words: NumPy, array, element-wise, percentile, standard deviation, outlier.

Evidence: DA13.ipynb with the four numbers from both routes and a passing allclose check.

### Session 14. Exploring distributions with seaborn

Question: What does a typical sale look like, and does it differ between the three shops?

By the end: you can draw a histogram and a box plot with seaborn and describe the shape, the middle and the outliers of a column.

New library: seaborn.

Words: seaborn, exploratory analysis, distribution, box plot, skewed, group comparison.

Evidence: DA14.ipynb with a histogram, a box plot, three medians and a finding.

### Session 15. Exploring relationships: scatter plots, correlation and cause

Question: Do busier days bring in more money, and does rain keep customers away?

By the end: you can draw a scatter plot coloured by group, read a correlation number, and say why a correlation does not prove one thing causes another.

Words: correlation, strength, heatmap, hue, cause.

Evidence: DA15.ipynb with three correlations and a sentence on why correlation is not cause.


## Week 6. Messy data and two tables

Product of the week: Checkpoint two: clean, merge and reconcile, with the residual named.

### Session 16. Cleaning the raw export

Question: If we clean the raw export carefully, does it give back the true revenue?

By the end: you can turn a messy export into a clean table with a pipeline that reruns, and explain why its total is lower than the true total.

Words: parse, normalise, lookup, exclude, residual, pipeline.

Evidence: DA16.ipynb with the function, two passing asserts, and a sentence naming the residual of 125400 and its cause.

### Session 17. Merging two tables and the fan-out trap

Question: Which product category earns the most, and can we trust the merge that tells us?

By the end: you can merge two tables on a key, check the row count before and after, and spot a duplicated key that inflates a total.

Words: merge key, merge, left merge, unique, fan-out, reconcile.

Evidence: DA17.ipynb with the unchanged row count, three branch totals and the reconciliation sentence.

### Session 18. Checkpoint two: clean, merge and reconcile

Question: Which category earns the most in the cleaned data, and by how much do our totals fall short of the truth?

By the end: you can clean a raw export, merge it with a lookup table, and report a total together with its named difference from the true total.

Evidence: DA18.ipynb that reruns from a restarted kernel, with rows kept and excluded, the unique-key check, category totals, the named residual and two limitations. Marks follow ASSESSMENT_AND_SHOWCASE.md.


## Week 7. Show it

Product of the week: An approved project plan and a rerunnable notebook.

### Session 19. Project question and a safe plan

Question: Which three questions can our data answer, and how will we show the answers?

By the end: you can write a narrow project plan with a question, the data, the measures, the charts and the limits, and have it approved.

Words: project question, scope, data dictionary, limitation, licence, disclosure.

Evidence: PROJECT_PLAN.md approved by the instructor, with a data dictionary for the columns used.

### Session 20. Build a reliable analysis

Question: Can a stranger follow my steps from the raw file to my numbers?

By the end: you can build the calculations for your project so that each one is checked by hand and by a second route, and a partner can rerun them.

Evidence: A notebook that reruns from the top, a cleaning log, and a partner note recording one rerun and the first discrepancy fixed.

### Session 21. Build and test the chart report

Question: Does my report answer my questions without a verbal tour?

By the end: you can build a chart report that a stranger reads in 30 seconds, and you can critique a coding assistant's hint with a test.

Words: chart report, caption, data source note.

Evidence: A chart report whose headline numbers match the notebook, a peer note on where they hesitated, and AI_USE_LOG.md with the tested critique.


## Week 8. Hand over

Product of the week: The report, the five-minute talk and the unaided demonstration.

### Session 22. Report and handover

Question: Does everything I submit open, rerun and agree with itself?

By the end: you can hand over a project that another person can open, rerun and check.

Evidence: All five files submitted and reopened, and totals in the report that agree with the notebook.

### Session 23. Explain it to a parent

Question: Can a parent say what I found, how I know, and what the data cannot tell us?

By the end: you can explain your project to a listener who has never seen code, in five minutes, with a chart and a limit.

Evidence: showcase.pptx and a PDF backup, a timed rehearsal and a feedback note from a peer.

### Session 24. Parent showcase and next steps

Question: What can I show and explain, and what will I learn next?

By the end: you can present your project, answer questions, and change a small part of it live without AI assistance.

Evidence: A completed demonstration, one unaided change, feedback and a recorded completion decision. Attendance is recorded separately from competence.
