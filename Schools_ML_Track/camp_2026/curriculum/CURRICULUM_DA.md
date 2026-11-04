# Python for Data Analysis: curriculum

Eight weeks, three core sessions a week, 24 core sessions, each proposed at three hours including a 15-minute break. Audience: S.4 to S.6 students and school leavers. No programming, spreadsheet or statistics experience is assumed. Each week ends with a badge on the learner's My_Progress_Map.pdf. Every session has a "Where this is used" hook, and every learner grows one personal project from week 1. Confirm session length and dates before advertising hour totals.


## Week 1. Meet the data (badge: First Look)

Product of the week: A notebook that reads the shop table and an error log.

### Session 1. Open a notebook and read your first table

Question: What does one week of sales in a small shop look like?

Where this is used: Supermarkets, mobile money agents and clinics all start the day by opening a table of what happened yesterday. Today you open your first one, from a small shop. What would you most want to know about a shop after seeing one week of its sales?

By the end: you can open, run, save and reopen a notebook, and read a table of shop sales into it.

New library: pandas.

Words: notebook, cell, run, output, file, table.

Saved in your build log: DA01.ipynb that reopens with the nickname, 11 and three table rows.

### Session 2. Values, names and types

Question: What kind of thing is each part of a sale?

Where this is used: A till keeps a product name as text, a price as a number and a date as a date. If the types get mixed up, the totals go wrong. Which one is a phone number: text or a number?

By the end: you can store numbers and text under names, and say what type each one is.

Words: value, integer, float, string, variable, type.

Saved in your build log: DA02.ipynb with the total 5001.0 and a sentence about the quotation marks.

### Session 3. Arithmetic, revenue and reading errors

Question: How much money did the first three sales bring in?

Where this is used: Revenue is units times price, added up. A shop owner does it by hand, and a program does it for every sale in a blink. Which error message have you seen on your phone, and what did it mean?

By the end: you can calculate revenue for a sale, check it by hand, and read an error message to find the line to fix.

Words: operator, expression, order of operations, comment, error message, line number.

Saved in your build log: DA03.ipynb with 50.0, the prediction written before the run, and an error log with two errors read correctly.


## Week 2. Python you need (badge: Code Builder)

Product of the week: Three small Python programs with checks that pass.

### Session 4. Conditions and decisions

Question: Is this sale big enough to count as a large order?

Where this is used: Shops and delivery businesses often treat big orders differently, with free delivery, a discount or a call from the manager. A program makes that choice with if and else. What rule would you set for the big orders of your own shop?

By the end: you can write a decision that gives a different answer for True and False, and test it at the edge.

Words: comparison, Boolean, if, else, indentation, and, or.

Saved in your build log: DA04.ipynb with the decision tested at 4999, 5000 and 5001.

### Session 5. Lists, dictionaries and loops

Question: How many units did the first six sales sell in total?

Where this is used: A shop has many sales, a league has many matches and a tailor has many orders. A loop handles every one of them without you typing each by hand. What would you loop over in your favourite sport?

By the end: you can store several values in a list, look one up by position, and use a loop to add them up.

Words: list, index, dictionary, key, loop, running total.

Saved in your build log: DA05.ipynb with the loop output 3, 5, 7, the stock 8 and the explanation of position 0.

### Session 6. Functions and checks that fail loudly

Question: Can we trust our revenue calculation on cases we already know the answer to?

Where this is used: Payment and tax software relies on functions that must give the right answer on cases where the answer is already known. A check that fails loudly protects every customer. What known case would you use to test a discount function?

By the end: you can write a function that returns a result, and use assert to check it on known cases.

Words: function, parameter, argument, return, assert, edge case.

Saved in your build log: DA06.ipynb with the function and three passing asserts, rerun from the top.


## Week 3. Tables in pandas (badge: Table Tamer)

Product of the week: Revenue by item and by branch, checked against the hand total.

### Session 7. A table in Python: DataFrame, columns and reading a CSV

Question: What is in each table we have been given?

Where this is used: Till exports, clinic registers and school timetables all become tables in Python. This is the table every data analyst works with. Which exported file would you most like to open?

By the end: you can build a small table, read a CSV file into one, and say how many rows and columns it has and what each column holds.

New library: pandas.

Words: row, column, header, CSV, DataFrame, library.

Saved in your build log: DA07.ipynb with shape (1513, 6), the six column names and two sentences naming the date and price columns.

### Session 8. Select, filter and calculate a revenue column

Question: How much money did the practice shop take in, and where did it come from?

Where this is used: A shop owner asks which sales were big and how much money they brought in. Picking out rows and adding a new column is how analysts answer that on their own data. Which rows of a shop table would you pick out first?

By the end: you can pick a column, keep the rows that meet a condition, and add a revenue column.

Words: select, filter, mask, new column, revenue, sum.

Saved in your build log: DA08.ipynb with 14 sales, 90000 shillings and a sentence on the difference.

### Session 9. Sort, group, mean and median

Question: Which item earns the most, and what is a typical sale in a small practice shop?

Where this is used: Retail chains compare their branches by grouping sales and finding the best sellers. A typical sale and an unusually large one tell different stories. Which branch would you visit first, and why?

By the end: you can total a column by group, sort the result, and say when the median describes a column better than the mean.

Words: group, sort, mean, median, proportion, denominator.

Saved in your build log: DA09.ipynb with three sorted totals that add to 6375900 and a passing assert.


## Week 4. Clean and chart (badge: Clean and Chart)

Product of the week: Your first chart: a cleaned table, three labelled charts, findings.

### Session 10. Cleaning without hiding evidence

Question: What is wrong with the raw Sunrise sales file, and how many rows does each problem touch?

Where this is used: Exports from tills often hold duplicates, blanks and typing slips. Good analysts keep a log of every fix so the owner can trust the result. How many problems can you find before you fix a single one?

By the end: you can find missing values and duplicates, remove the duplicates on a copy, and save a cleaning log that says what you did.

Words: raw data, missing value, duplicate, data type, copy, cleaning log.

Saved in your build log: DA10.ipynb and my_log.csv with the three counts and the sentence about zero.

### Session 11. Charts that say what the numbers say

Question: Which chart shows this comparison most clearly?

Where this is used: Weather pages, football stats and mobile money summaries all lean on a chart to make one point quickly. A busy shop owner has a minute at most. Which chart would you show an owner who has only one minute?

By the end: you can draw a bar chart, a line chart, a histogram and a scatter plot with labelled axes, and state one finding and one limit for each.

New library: matplotlib.

Words: matplotlib, bar chart, line chart, histogram, scatter plot, axis label.

Saved in your build log: DA11.ipynb with a labelled bar chart of three branches, one finding and one limitation.

### Session 12. Show your first chart and explain what it says

Question: What do the Sunrise Shops sales tell us about the three shops?

Where this is used: Every analyst sends someone a first report: a table, one chart and a few honest sentences. Today you make yours. Who would you most like to send it to?

By the end: you can read a table, check it, summarise it, chart it and explain two findings and one limit, from a restarted notebook.

Saved in your build log: DA12.ipynb that reruns from a restarted kernel, with the rows, total, checks, sorted branch totals, one labelled chart, two findings and one limitation. It goes in the build log, and the instructor gives one strength and one next step in a private chat.


## Week 5. Explore with NumPy and seaborn (badge: Pattern Spotter)

Product of the week: Spread, distributions and relationships explored, with what each shows.

### Session 13. NumPy: the numbers underneath pandas

Question: How spread out are the daily customer counts, and which sales are unusually large?

Where this is used: Weather offices and football analysts work with long rows of numbers, such as daily rainfall or distance run. They check how spread out the numbers are and spot unusual days. Which day in a shop would you call unusual?

By the end: you can turn a column into a NumPy array, calculate its mean, median, spread and percentiles, and find unusually large values.

New library: NumPy.

Words: NumPy, array, element-wise, percentile, standard deviation, outlier.

Saved in your build log: DA13.ipynb with the four numbers from both routes and a passing allclose check.

### Session 14. Exploring distributions with seaborn

Question: What does a typical sale look like, and does it differ between the three shops?

Where this is used: A histogram shows what a typical day looks like, and a box plot shows how groups differ. Club analysts compare players and teams with plots like these. Which two shops would you compare first?

By the end: you can draw a histogram and a box plot with seaborn and describe the shape, the middle and the outliers of a column.

New library: seaborn.

Words: seaborn, exploratory analysis, distribution, box plot, skewed, group comparison.

Saved in your build log: DA14.ipynb with a histogram, a box plot, three medians and a finding.

### Session 15. Exploring relationships: scatter plots, correlation and cause

Question: Do busier days bring in more money, and does rain keep customers away?

Where this is used: Taxi parks, shops and farms all ask whether rain changes demand. Two things moving together do not prove that one causes the other. Do rainy days keep customers away, or is something else going on?

By the end: you can draw a scatter plot coloured by group, read a correlation number, and say why a correlation does not prove one thing causes another.

Words: correlation, strength, heatmap, hue, cause.

Saved in your build log: DA15.ipynb with three correlations and a sentence on why correlation is not cause.


## Week 6. Messy data and two tables (badge: Truth Finder)

Product of the week: A cleaned and merged table, reconciled with the residual named.

### Session 16. Cleaning the raw export

Question: If we clean the raw export carefully, does it give back the true revenue?

Where this is used: A raw export from a real system is rarely tidy. Analysts clean it with a function so the same steps run again on next month's file. Could you clean a file you have never seen?

By the end: you can turn a messy export into a clean table with a pipeline that reruns, and explain why its total is lower than the true total.

Words: parse, normalise, lookup, exclude, residual, pipeline.

Saved in your build log: DA16.ipynb with the function, two passing asserts, and a sentence naming the residual of 125400 and its cause.

### Session 17. Merging two tables and the fan-out trap

Question: Which product category earns the most, and can we trust the merge that tells us?

Where this is used: Customers, products and sales usually live in separate tables, and analysts join them. A careless join can count one sale twice. How would you check that your total is still right after a join?

By the end: you can merge two tables on a key, check the row count before and after, and spot a duplicated key that inflates a total.

Words: merge key, merge, left merge, unique, fan-out, reconcile.

Saved in your build log: DA17.ipynb with the unchanged row count, three branch totals and the reconciliation sentence.

### Session 18. Does your total match the true total? Clean, merge and reconcile

Question: Which category earns the most in the cleaned data, and by how much do our totals fall short of the truth?

Where this is used: Accountants and auditors compare two totals and explain the gap. Banks and tax teams do this every month. Can you explain why your total is a little short of the true one?

By the end: you can clean a raw export, merge it with a lookup table, and report a total together with its named difference from the true total.

Saved in your build log: DA18.ipynb that reruns from a restarted kernel, with rows kept and excluded, the unique-key check, category totals, the named residual and two limitations. It goes in the build log, and the instructor gives one strength and one next step in a private chat.


## Week 7. Show it (badge: Project Builder)

Product of the week: An approved project plan and a rerunnable notebook.

### Session 19. Project question and a safe plan

Question: Which three questions can our data answer, and how will we show the answers?

Where this is used: Data teams write a short plan before any code: the question, the data, the charts and what the data cannot say. Which three questions about a topic you love could a table answer?

By the end: you can write a narrow project plan with a question, the data, the measures, the charts and the limits, and have it approved.

Words: project question, scope, data dictionary, limitation, licence, disclosure.

Saved in your build log: PROJECT_PLAN.md approved by the instructor, with a data dictionary for the columns used.

### Session 20. Build a reliable analysis

Question: Can a stranger follow my steps from the raw file to my numbers?

Where this is used: A result is only useful if someone else can repeat it. Analysts log each step and check each number two ways. Who could rerun your analysis and get the same numbers?

By the end: you can build the calculations for your project so that each one is checked by hand and by a second route, and a partner can rerun them.

Saved in your build log: A notebook that reruns from the top, a cleaning log, and a partner note recording one rerun and the first discrepancy fixed.

### Session 21. Build and check the chart report

Question: Does my report answer my questions without a verbal tour?

Where this is used: A report that needs its author in the room has not done its job. Clear titles, labels and units let a farmer, a manager or a parent read it alone. Could your report speak for itself?

By the end: you can build a chart report that a stranger reads in 30 seconds, and you can critique a coding assistant's hint with a test.

Words: chart report, caption, data source note.

Saved in your build log: A chart report whose headline numbers match the notebook, a peer note on where they hesitated, and AI_USE_LOG.md with the tested critique.


## Week 8. Hand over (badge: Showcase)

Product of the week: The report, the five-minute talk and the parent showcase.

### Session 22. Report and handover

Question: Does everything I share open, rerun and agree with itself?

Where this is used: Before a team hands work over, they restart everything and run it from the top to prove it works. A tidy handover saves other people days. Does your notebook run from the first cell to the last?

By the end: you can hand over a project that another person can open, rerun and check.

Saved in your build log: All five files saved together and reopened, and totals in the report that agree with the notebook.

### Session 23. Explain it to a parent

Question: Can a parent say what I found, how I know, and what the data cannot tell us?

Where this is used: Analysts explain their findings to busy people who do not write code. They say what they found, how they know, and what the data cannot tell. How would you say it to a parent in one minute?

By the end: you can explain your project to a listener who has never seen code, in five minutes, with a chart and a limit.

Saved in your build log: showcase.pptx and a PDF backup, a timed rehearsal and a feedback note from a peer.

### Session 24. Parent showcase and next steps

Question: What can I show and explain, and what will I learn next?

Where this is used: Start-ups and tech hubs hold demo days where builders show what they made and answer questions. Today is your demo day. What do you want your family to remember about your work?

By the end: you can present your project, answer questions, and try a small change to it live with no AI assistant open.

Saved in your build log: A showcase talk, one small live change, one strength and one next step, and a certificate decision based on attendance, build log and finished project.
