# DA S14 Getting data in and modelling it

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Getting data in, and modelling it

TEACHING PURPOSE
Getting data in, and modelling it

LECTURER CUE
Start on time.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Getting data in, and modelling it.

LECTURER CUE
Tonight is session 14 of fifteen.

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
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
Why does a Power BI total come out wrong. Move on after a learner can explain the current example or required action.

## Slide 5 — Why does a Power BI total come out wrong

TEACHING PURPOSE
Why does a Power BI total come out wrong

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Almost always the model: one relationship pointing the wrong way, or no date table.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Power Query: get it in, shape it, keep the recipe. Move on after a learner can explain the current example or required action.

## Slide 6 — Power Query: get it in, shape it, keep the recipe

TEACHING PURPOSE
Power Query: get it in, shape it, keep the recipe

CONNECT
Build on the preceding slide: Why does a Power BI total come out wrong.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Power BI is three products, and people confuse them. Move on after a learner can explain the current example or required action.

## Slide 7 — Power BI is three products, and people confuse them

TEACHING PURPOSE
Power BI is three products, and people confuse them

CONNECT
Build on the preceding slide: Power Query: get it in, shape it, keep the recipe.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
A data model. Move on after a learner can explain the current example or required action.

## Slide 8 — A data model

TEACHING PURPOSE
A data model

CONNECT
Build on the preceding slide: Power BI is three products, and people confuse them.

LECTURER CUE
The tables plus the relationships between them, defined once, so you do not write a join in every query.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
A star schema. Move on after a learner can explain the current example or required action.

## Slide 9 — A star schema

TEACHING PURPOSE
A star schema

CONNECT
Build on the preceding slide: A data model.

LECTURER CUE
One fact table in the middle holding the events, with dimension tables around it holding the descriptions you slice by. Every dimension points INTO the fact, one-to-many.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
A date table. Move on after a learner can explain the current example or required action.

## Slide 10 — A date table

TEACHING PURPOSE
A date table

CONNECT
Build on the preceding slide: A star schema.

LECTURER CUE
A separate table with one row per date, marked as the date table and related to your fact's date column.

NEXT
The date table, and the step everybody skips. Move on after a learner can explain the current example or required action.

## Slide 11 — The date table, and the step everybody skips

TEACHING PURPOSE
The date table, and the step everybody skips

CONNECT
Build on the preceding slide: A date table.

EXPLAIN IN ORDINARY WORDS
A seasonal pattern repeats at calendar intervals. Compare like periods before calling a change growth; compare counts, coverage and definitions as well.

CHECK AND EXPECTED ANSWER
Does a rise from November to December prove underlying growth? No; compare comparable Decembers and inspect the wider series.

IF LEARNERS ARE STUCK
Draw a two-year timeline and match the same months. Separate description from an explanation of cause.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: The date table, and the step everybody skips.

LECTURER CUE
Ten minutes.

NEXT
The model, which is where the marks are. Move on after a learner can explain the current example or required action.

## Slide 13 — The model, which is where the marks are

TEACHING PURPOSE
The model, which is where the marks are

CONNECT
Build on the preceding slide: Break.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
What you are building tonight. Move on after a learner can explain the current example or required action.

## Slide 14 — What you are building tonight

TEACHING PURPOSE
What you are building tonight

CONNECT
Build on the preceding slide: The model, which is where the marks are.

LECTURER CUE
The same six tables you mapped by hand in session 2, now as a model. The arrows all point the same way: many orders to one customer. Row counts are the real ones.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Build these five relationships by hand. Move on after a learner can explain the current example or required action.

## Slide 15 — Build these five relationships by hand

TEACHING PURPOSE
Build these five relationships by hand

CONNECT
Build on the preceding slide: What you are building tonight.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Reconcile against numbers you already have. Move on after a learner can explain the current example or required action.

## Slide 16 — Reconcile against numbers you already have

TEACHING PURPOSE
Reconcile against numbers you already have

CONNECT
Build on the preceding slide: Build these five relationships by hand.

LECTURER CUE
Reference.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Before you start tonight. Move on after a learner can explain the current example or required action.

## Slide 17 — Before you start tonight

TEACHING PURPOSE
Before you start tonight

CONNECT
Build on the preceding slide: Reconcile against numbers you already have.

LECTURER CUE
Power BI Desktop requires Windows. Rehearse the browser semantic-model editor and Power Query with the actual learner account, workspace permissions and tenant settings. Use the CSV lab route; arrange a Windows lab machine if browser editing is unavailable.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Trusting the relationships Power BI detects for you. Check every direction, then check a total against a number you already trust.. Move on after a learner can explain the current example or required action.

## Slide 18 — Trusting the relationships Power BI detects for you. Check every direction, then check a total against a number you already trust.

TEACHING PURPOSE
Trusting the relationships Power BI detects for you. Check every direction, then check a total against a number you already trust.

CONNECT
Build on the preceding slide: Before you start tonight.

LECTURER CUE
Trusting the relationships Power BI detects for you. Check every direction, then check a total against a number you already trust.

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
Build on the preceding slide: Trusting the relationships Power BI detects for you. Check every direction, then check a total against a number you already trust..

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Why a flat table is wrong
It cannot represent something that did not happen. A customer who bought nothing this quarter and a month with no orders both vanish, because the only rows that exist are rows where something occurred. This is session 2, arriving again.
B
Months sorting alphabetically
The Month column is text and has not been told to sort by MonthNo. Column tools, Sort by column, MonthNo. It is not a bug.
C
Revenue three times too big
Fan-out from a relationship, which is session 5's trap in a new tool. Check the direction and cardinality of every one, especially any you did not build yourself.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

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
Load it, model it, reconcile it. Move on after a learner can explain the current example or required action.

## Slide 21 — Load it, model it, reconcile it

TEACHING PURPOSE
Load it, model it, reconcile it

CONNECT
Build on the preceding slide: How did you do?.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Load it, model it, reconcile it continued. Move on after a learner can explain the current example or required action.

## Slide 22 — Load it, model it, reconcile it continued

TEACHING PURPOSE
Load it, model it, reconcile it continued

CONNECT
Build on the preceding slide: Load it, model it, reconcile it.

LECTURER CUE
Five tables in, five relationships built by hand, a date table marked and sorted, and three visuals whose totals match the numbers you already got from SQL and pandas. Reconciliation is your practice check.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 23 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Load it, model it, reconcile it continued.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 24 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Add the Uganda Healthsites file and put a map visual on it. Notice what that file makes easy and what it makes impossible.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

NEXT
The model decides whether the report is true. Move on after a learner can explain the current example or required action.

## Slide 25 — The model decides whether the report is true

TEACHING PURPOSE
The model decides whether the report is true

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Visuals are half an hour of work. The model is the difference between a dashboard and a liability. Get the arrows right, then make it look good.

EXPLAIN IN ORDINARY WORDS
Begin with the question and intended comparison. Identify what an axis, bar, point or colour represents, including its unit. A chart summarises data and may hide variation.

CHECK AND EXPECTED ANSWER
For a bar chart comparing amounts, why normally start the value axis at zero? Bar length encodes magnitude; truncation can exaggerate differences.

IF LEARNERS ARE STUCK
Read one mark aloud as a sentence. Check the population, period, filters and units before stating the finding.

