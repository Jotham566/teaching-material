# DA S05 Joining tables carefully

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Joining tables, carefully

TEACHING PURPOSE
Joining tables, carefully

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Joining tables, carefully.

LECTURER CUE
Tonight is session 5 of fifteen.

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
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

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
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Your total went up when you joined a table.. Move on after a learner can explain the current example or required action.

## Slide 5 — Your total went up when you joined a table.

TEACHING PURPOSE
Your total went up when you joined a table.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Yes, and it is wrong. A join can multiply rows, and nothing warns you except a row count you were not watching.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
INNER and LEFT, and the row count that tells you. Move on after a learner can explain the current example or required action.

## Slide 6 — INNER and LEFT, and the row count that tells you

TEACHING PURPOSE
INNER and LEFT, and the row count that tells you

CONNECT
Build on the preceding slide: Your total went up when you joined a table..

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
INNER JOIN. Move on after a learner can explain the current example or required action.

## Slide 7 — INNER JOIN

TEACHING PURPOSE
INNER JOIN

CONNECT
Build on the preceding slide: INNER and LEFT, and the row count that tells you.

LECTURER CUE
Keep only the rows that matched on both sides. Anything without a match disappears, with no message.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
LEFT JOIN. Move on after a learner can explain the current example or required action.

## Slide 8 — LEFT JOIN

TEACHING PURPOSE
LEFT JOIN

CONNECT
Build on the preceding slide: INNER JOIN.

LECTURER CUE
Keep every row on the left, and leave the right-hand columns empty where nothing matched.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Fan-out. Move on after a learner can explain the current example or required action.

## Slide 9 — Fan-out

TEACHING PURPOSE
Fan-out

CONNECT
Build on the preceding slide: LEFT JOIN.

LECTURER CUE
When one row matches several rows, its values are repeated once per match. Sum them afterwards and you have counted the same thing several times.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
CTE. Move on after a learner can explain the current example or required action.

## Slide 10 — CTE

TEACHING PURPOSE
CTE

CONNECT
Build on the preceding slide: Fan-out.

LECTURER CUE
A named step at the top of a query that you can then use like a table. Short for common table expression, and nobody says that out loud.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Watch the row count decide the answer. Move on after a learner can explain the current example or required action.

## Slide 11 — Watch the row count decide the answer

TEACHING PURPOSE
Watch the row count decide the answer

CONNECT
Build on the preceding slide: CTE.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Watch the row count decide the answer.

LECTURER CUE
Ten minutes.

NEXT
Fan-out, and queries somebody else can read. Move on after a learner can explain the current example or required action.

## Slide 13 — Fan-out, and queries somebody else can read

TEACHING PURPOSE
Fan-out, and queries somebody else can read

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Fan-out, made visible. Move on after a learner can explain the current example or required action.

## Slide 14 — Fan-out, made visible

TEACHING PURPOSE
Fan-out, made visible

CONNECT
Build on the preceding slide: Fan-out, and queries somebody else can read.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Three named steps instead of one long query. Move on after a learner can explain the current example or required action.

## Slide 15 — Three named steps instead of one long query

TEACHING PURPOSE
Three named steps instead of one long query

CONNECT
Build on the preceding slide: Fan-out, made visible.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
The report the sales manager actually wants. Move on after a learner can explain the current example or required action.

## Slide 16 — The report the sales manager actually wants

TEACHING PURPOSE
The report the sales manager actually wants

CONNECT
Build on the preceding slide: Three named steps instead of one long query.

LECTURER CUE
Revenue by rep by month for 2025, net of returns. Two CTEs and a final SELECT, built and checked one step at a time.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Checkpoint 1. Move on after a learner can explain the current example or required action.

## Slide 17 — Checkpoint 1

TEACHING PURPOSE
Checkpoint 1

CONNECT
Build on the preceding slide: The report the sales manager actually wants.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
A join that multiplies rows. The total gets bigger and looks plausible, and the only tell is the row count.. Move on after a learner can explain the current example or required action.

## Slide 18 — A join that multiplies rows. The total gets bigger and looks plausible, and the only tell is the row count.

TEACHING PURPOSE
A join that multiplies rows. The total gets bigger and looks plausible, and the only tell is the row count.

CONNECT
Build on the preceding slide: Checkpoint 1.

LECTURER CUE
A join that multiplies rows. The total gets bigger and looks plausible, and the only tell is the row count.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 19 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: A join that multiplies rows. The total gets bigger and looks plausible, and the only tell is the row count..

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Same count from INNER and LEFT
Every row on the left found a match, so on today's data the two are equivalent. That is a fact about these rows rather than about the tables, so re-check it when the data changes.
B
Summing a per-order figure after joining to lines
Fan-out. The order-level figure repeated once per line, so the total counted it several times: 6,000 orders became 20,234 rows. Aggregate the lines first, in their own step, then join.
C
Why CTEs rather than nesting
You can run a CTE on its own and check it. A nested subquery can only be checked as part of the whole thing, which means a mistake in the middle is the last one you find.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 20 — How did you do?

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
Build the rep revenue report. Move on after a learner can explain the current example or required action.

## Slide 21 — Build the rep revenue report

TEACHING PURPOSE
Build the rep revenue report

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
This is Checkpoint 1 and it is marked against the answer key tonight. Build it as named steps and check the row count after each one.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 22 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Build the rep revenue report.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 23 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Finish the report if it is not finished, then break it on purpose: change one LEFT JOIN to an INNER JOIN and write down what changed in the numbers and why.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
The row count is the smoke alarm. Move on after a learner can explain the current example or required action.

## Slide 24 — The row count is the smoke alarm

TEACHING PURPOSE
The row count is the smoke alarm

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Every error in this session announced itself the same way: a count that changed when you did not expect it to. Nothing else warns you, so build the habit now while the data is still small enough to check by hand.

