# DA S03 Asking a database for rows

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Asking a database for rows

TEACHING PURPOSE
Asking a database for rows

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Asking a database for rows.

LECTURER CUE
Tonight is session 3 of fifteen.

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
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

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
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
How do you ask a database for exactly the rows you want,. Move on after a learner can explain the current example or required action.

## Slide 5 — How do you ask a database for exactly the rows you want,

TEACHING PURPOSE
How do you ask a database for exactly the rows you want,

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Every clause you add changes the row count. The row count is how you check yourself.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
A query is a written-down filter. Move on after a learner can explain the current example or required action.

## Slide 6 — A query is a written-down filter

TEACHING PURPOSE
A query is a written-down filter

CONNECT
Build on the preceding slide: How do you ask a database for exactly the rows you want,.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
A query. Move on after a learner can explain the current example or required action.

## Slide 7 — A query

TEACHING PURPOSE
A query

CONNECT
Build on the preceding slide: A query is a written-down filter.

LECTURER CUE
A written description of the rows you want. You describe the result and the database works out how to fetch it, which is why SQL has outlived every tool built on top of it.

NEXT
NULL. Move on after a learner can explain the current example or required action.

## Slide 8 — NULL

TEACHING PURPOSE
NULL

CONNECT
Build on the preceding slide: A query.

LECTURER CUE
No value recorded. It is not zero and it is not an empty piece of text. Any comparison with NULL is neither true nor false, so a filter written with = NULL matches nothing at all.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Build it one clause at a time, watching the row count. Move on after a learner can explain the current example or required action.

## Slide 9 — Build it one clause at a time, watching the row count

TEACHING PURPOSE
Build it one clause at a time, watching the row count

CONNECT
Build on the preceding slide: NULL.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 10 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Build it one clause at a time, watching the row count.

LECTURER CUE
Ten minutes.

NEXT
Nothing, zero, and blank are three different things. Move on after a learner can explain the current example or required action.

## Slide 11 — Nothing, zero, and blank are three different things

TEACHING PURPOSE
Nothing, zero, and blank are three different things

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
The one that catches everybody. Move on after a learner can explain the current example or required action.

## Slide 12 — The one that catches everybody

TEACHING PURPOSE
The one that catches everybody

CONNECT
Build on the preceding slide: Nothing, zero, and blank are three different things.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Your first real answer, in four steps. Move on after a learner can explain the current example or required action.

## Slide 13 — Your first real answer, in four steps

TEACHING PURPOSE
Your first real answer, in four steps

CONNECT
Build on the preceding slide: The one that catches everybody.

LECTURER CUE
How much revenue did we take on delivered orders? Revenue is not a column: it is quantity times price times one minus discount, and it lives on the order lines.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Writing = NULL instead of IS NULL. No error, no warning, zero rows, and the zero looks like a fact about the business.. Move on after a learner can explain the current example or required action.

## Slide 14 — Writing = NULL instead of IS NULL. No error, no warning, zero rows, and the zero looks like a fact about the business.

TEACHING PURPOSE
Writing = NULL instead of IS NULL. No error, no warning, zero rows, and the zero looks like a fact about the business.

CONNECT
Build on the preceding slide: Your first real answer, in four steps.

LECTURER CUE
Writing = NULL instead of IS NULL. No error, no warning, zero rows, and the zero looks like a fact about the business.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 15 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Writing = NULL instead of IS NULL. No error, no warning, zero rows, and the zero looks like a fact about the business..

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
COUNT(*) against COUNT(city)
COUNT(*) counts rows. COUNT(city) counts rows where city is not NULL. On orders that difference is 172 rows, worth UGX 390,632,335.
B
Why = NULL matches nothing
Because NULL means no value, and comparing anything with no value is neither true nor false. The filter is never satisfied. IS NULL is a different test and it works.
C
The first question about any revenue figure
Which orders does it count? Delivered only is UGX 8,751,705,520; everything is UGX 10,758,894,480. The gap is UGX 2,007,188,960, and nobody can tell which you meant from the number alone.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 16 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Eight questions against the database. Move on after a learner can explain the current example or required action.

## Slide 17 — Eight questions against the database

TEACHING PURPOSE
Eight questions against the database

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Work them in order; they get harder. Every question has its answer on the sheet, so you know within seconds whether you are right. Write the query before you look at the answer: reading it first feels like learning and is not.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 18 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Eight questions against the database.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 19 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Five more questions on the sheet. Then: name one table at work you would like to query, and write down what its columns probably are.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Check the row count after every clause. Move on after a learner can explain the current example or required action.

## Slide 20 — Check the row count after every clause

TEACHING PURPOSE
Check the row count after every clause

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
It is the cheapest habit in this course and it catches most wrong answers before they leave your screen. A number that moved when you did not expect it to is telling you something you need to know.

