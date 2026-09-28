# DA S09 Grouping and joining in pandas

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Grouping and joining in pandas

TEACHING PURPOSE
Grouping and joining in pandas

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
Build on the preceding slide: Grouping and joining in pandas.

LECTURER CUE
Tonight is session 9 of fifteen.

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
Your SQL and your pandas give different answers.. Move on after a learner can explain the current example or required action.

## Slide 5 — Your SQL and your pandas give different answers.

TEACHING PURPOSE
Your SQL and your pandas give different answers.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Usually neither. They are answering slightly different questions, and finding out which is the actual skill.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
groupby: split, apply, combine. Move on after a learner can explain the current example or required action.

## Slide 6 — groupby: split, apply, combine

TEACHING PURPOSE
groupby: split, apply, combine

CONNECT
Build on the preceding slide: Your SQL and your pandas give different answers..

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
groupby. Move on after a learner can explain the current example or required action.

## Slide 7 — groupby

TEACHING PURPOSE
groupby

CONNECT
Build on the preceding slide: groupby: split, apply, combine.

LECTURER CUE
Split the rows into groups, apply an aggregation to each, combine the results into a new table. It is SQL's GROUP BY and it is your pivot table.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Index. Move on after a learner can explain the current example or required action.

## Slide 8 — Index

TEACHING PURPOSE
Index

CONNECT
Build on the preceding slide: groupby.

LECTURER CUE
The labels down the side of a DataFrame. After a groupby your grouping keys become the index rather than columns, which is the commonest confusion in pandas.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
merge, and validate. Move on after a learner can explain the current example or required action.

## Slide 9 — merge, and validate

TEACHING PURPOSE
merge, and validate

CONNECT
Build on the preceding slide: Index.

LECTURER CUE
merge is pandas' join. validate is the argument that makes it REFUSE a join that would multiply rows instead of silently doing it.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
groupby, and the four characters that fix it. Move on after a learner can explain the current example or required action.

## Slide 10 — groupby, and the four characters that fix it

TEACHING PURPOSE
groupby, and the four characters that fix it

CONNECT
Build on the preceding slide: merge, and validate.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 11 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: groupby, and the four characters that fix it.

LECTURER CUE
Ten minutes.

NEXT
merge, and reconciling two tools. Move on after a learner can explain the current example or required action.

## Slide 12 — merge, and reconciling two tools

TEACHING PURPOSE
merge, and reconciling two tools

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
merge, with the guard rails on. Move on after a learner can explain the current example or required action.

## Slide 13 — merge, with the guard rails on

TEACHING PURPOSE
merge, with the guard rails on

CONNECT
Build on the preceding slide: merge, and reconciling two tools.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
The same three tables meeting, so region and month exist. Move on after a learner can explain the current example or required action.

## Slide 14 — The same three tables meeting, so region and month exist

TEACHING PURPOSE
The same three tables meeting, so region and month exist

CONNECT
Build on the preceding slide: merge, with the guard rails on.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Reconciling two tools, properly. Move on after a learner can explain the current example or required action.

## Slide 15 — Reconciling two tools, properly

TEACHING PURPOSE
Reconciling two tools, properly

CONNECT
Build on the preceding slide: The same three tables meeting, so region and month exist.

LECTURER CUE
Same question, same data, different tool. They have to agree, and where they do not you have found something.

EXPLAIN IN ORDINARY WORDS
A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.

CHECK AND EXPECTED ANSWER
Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.

IF LEARNERS ARE STUCK
Make two rows and two category columns by hand before showing the encoder.

NEXT
Checkpoint 2. Move on after a learner can explain the current example or required action.

## Slide 16 — Checkpoint 2

TEACHING PURPOSE
Checkpoint 2

CONNECT
Build on the preceding slide: Reconciling two tools, properly.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

NEXT
A merge that silently multiplies rows. validate turns that into an exception instead of a wrong number.. Move on after a learner can explain the current example or required action.

## Slide 17 — A merge that silently multiplies rows. validate turns that into an exception instead of a wrong number.

TEACHING PURPOSE
A merge that silently multiplies rows. validate turns that into an exception instead of a wrong number.

CONNECT
Build on the preceding slide: Checkpoint 2.

LECTURER CUE
A merge that silently multiplies rows. validate turns that into an exception instead of a wrong number.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 18 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: A merge that silently multiplies rows. validate turns that into an exception instead of a wrong number..

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
Cannot select a column you can see
It is in the index, not the columns. .reset_index() moves the grouping keys back and everything downstream works.
B
A merge that multiplied the rows
Fan-out: the right-hand side had several rows per key, so every left row was repeated once per match. Pass validate="one_to_many" and pandas raises instead. Aggregate the many side first, then merge.
C
A gap between SQL and pandas
The filters, first and always: status, the date window, and whether one side dropped the 172 rows with no customer. That last one alone is UGX 390,632,335. Only look at the arithmetic once the row sets match.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

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
Reconcile pandas against SQL. Move on after a learner can explain the current example or required action.

## Slide 20 — Reconcile pandas against SQL

TEACHING PURPOSE
Reconcile pandas against SQL

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Rebuild the rep revenue report in pandas and set it beside your SQL output. Any difference is a finding, and finding one is a pass. A clean match you cannot explain is not.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 21 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Reconcile pandas against SQL.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 22 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Take one report somebody at work produces by hand every month and write the pandas that would produce it. It does not have to run yet.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
Two tools, one answer. Move on after a learner can explain the current example or required action.

## Slide 23 — Two tools, one answer

TEACHING PURPOSE
Two tools, one answer

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Getting the same number twice, two different ways, is the only self-check available to somebody working alone. It is also the first thing you will be asked for when a number of yours is doubted.

