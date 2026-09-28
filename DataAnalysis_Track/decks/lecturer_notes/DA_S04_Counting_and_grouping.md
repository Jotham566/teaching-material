# DA S04 Counting and grouping

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Counting and grouping

TEACHING PURPOSE
Counting and grouping

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Counting and grouping.

LECTURER CUE
Tonight is session 4 of fifteen.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
The words for tonight. Move on after a learner can explain the current example or required action.

## Slide 3 — The words for tonight

TEACHING PURPOSE
The words for tonight

CONNECT
Build on the preceding slide: Where tonight sits.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
By the end of tonight you can…. Move on after a learner can explain the current example or required action.

## Slide 4 — By the end of tonight you can…

TEACHING PURPOSE
By the end of tonight you can…

CONNECT
Build on the preceding slide: The words for tonight.

LECTURER CUE
These three are what tonight is marked against, in the sense that the lab checks them.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
You can already build a pivot table.. Move on after a learner can explain the current example or required action.

## Slide 5 — You can already build a pivot table.

TEACHING PURPOSE
You can already build a pivot table.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
It runs again next month without you, somebody else can check it, and it works on files a spreadsheet will not open.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Your pivot table, written down. Move on after a learner can explain the current example or required action.

## Slide 6 — Your pivot table, written down

TEACHING PURPOSE
Your pivot table, written down

CONNECT
Build on the preceding slide: You can already build a pivot table..

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Aggregate. Move on after a learner can explain the current example or required action.

## Slide 7 — Aggregate

TEACHING PURPOSE
Aggregate

CONNECT
Build on the preceding slide: Your pivot table, written down.

LECTURER CUE
A calculation that collapses many rows into one number: count, sum, average, minimum, maximum.

NEXT
GROUP BY. Move on after a learner can explain the current example or required action.

## Slide 8 — GROUP BY

TEACHING PURPOSE
GROUP BY

CONNECT
Build on the preceding slide: Aggregate.

LECTURER CUE
Says which rows belong together before the aggregate runs. Group by region and you get one number per region.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
HAVING. Move on after a learner can explain the current example or required action.

## Slide 9 — HAVING

TEACHING PURPOSE
HAVING

CONNECT
Build on the preceding slide: GROUP BY.

LECTURER CUE
A filter on the GROUPS, applied after the aggregation. WHERE filters rows before grouping; HAVING filters the results afterwards.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Derived value. Move on after a learner can explain the current example or required action.

## Slide 10 — Derived value

TEACHING PURPOSE
Derived value

CONNECT
Build on the preceding slide: HAVING.

LECTURER CUE
A number the data does not store, computed from columns that it does.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
The same answer, both ways. Move on after a learner can explain the current example or required action.

## Slide 11 — The same answer, both ways

TEACHING PURPOSE
The same answer, both ways

CONNECT
Build on the preceding slide: Derived value.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: The same answer, both ways.

LECTURER CUE
Ten minutes.

NEXT
Filtering groups, and the trap in every average. Move on after a learner can explain the current example or required action.

## Slide 13 — Filtering groups, and the trap in every average

TEACHING PURPOSE
Filtering groups, and the trap in every average

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Revenue, which is not a column. Move on after a learner can explain the current example or required action.

## Slide 14 — Revenue, which is not a column

TEACHING PURPOSE
Revenue, which is not a column

CONNECT
Build on the preceding slide: Filtering groups, and the trap in every average.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
HAVING, after getting it wrong first. Move on after a learner can explain the current example or required action.

## Slide 15 — HAVING, after getting it wrong first

TEACHING PURPOSE
HAVING, after getting it wrong first

CONNECT
Build on the preceding slide: Revenue, which is not a column.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
When averaging averages gives a wrong result. Move on after a learner can explain the current example or required action.

## Slide 16 — When averaging averages gives a wrong result

TEACHING PURPOSE
When averaging averages gives a wrong result

CONNECT
Build on the preceding slide: HAVING, after getting it wrong first.

LECTURER CUE
Four regions, four average order values. The national average is not the average of those four, and the gap is not small.

NEXT
Averaging an average. The average of four regional averages is not the national average unless the regions are the same size. Sum the top, sum the bottom, then divide.. Move on after a learner can explain the current example or required action.

## Slide 17 — Averaging an average. The average of four regional averages is not the national average unless the regions are the same size. Sum the top, sum the bottom, then divide.

TEACHING PURPOSE
Averaging an average. The average of four regional averages is not the national average unless the regions are the same size. Sum the top, sum the bottom, then divide.

CONNECT
Build on the preceding slide: When averaging averages gives a wrong result.

LECTURER CUE
Averaging an average. The average of four regional averages is not the national average unless the regions are the same size. Sum the top, sum the bottom, then divide.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 18 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Averaging an average. The average of four regional averages is not the national average unless the regions are the same size. Sum the top, sum the bottom, then divide..

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Why WHERE COUNT(*) > 80 fails
WHERE is evaluated before the rows are grouped, so no count exists yet. Filtering on an aggregate is what HAVING is for.
B
Regional totals not adding up
Grouping by region needs a join to customers, and the 172 walk-in orders have no customer to join to. They drop out silently, taking UGX 390,632,335 with them.
C
Average order value three times too small
You divided by the number of order LINES instead of the number of ORDERS. There are 20,234 lines and 6,000 orders. COUNT(DISTINCT order_id) is the fix, and it is the grain lesson from session 1 arriving in arithmetic.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 19 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Three groupings, then check them in Excel. Move on after a learner can explain the current example or required action.

## Slide 20 — Three groupings, then check them in Excel

TEACHING PURPOSE
Three groupings, then check them in Excel

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Revenue by channel, by segment and by month, delivered orders only. Then export the order lines to CSV, build the same three figures as pivot tables, and confirm they agree. Where they disagree, the SQL is usually right and the pivot has quietly included something.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 21 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Three groupings, then check them in Excel.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 22 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Two more groupings on the sheet, then one sentence: which grouping of your own work data would you most like to see, and which columns would it need?

NEXT
You have written your first pivot table down. Move on after a learner can explain the current example or required action.

## Slide 23 — You have written your first pivot table down

TEACHING PURPOSE
You have written your first pivot table down

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
It now runs again next month without you, on a file too big for a spreadsheet, and somebody else can read what you did. That is the whole argument for SQL and you have just made it yourself.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

