# DA S02 Why data lives in several tables

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Why data lives in several tables

TEACHING PURPOSE
Why data lives in several tables

LECTURER CUE
Start on time.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Why data lives in several tables.

LECTURER CUE
Tonight is session 2 of fifteen.

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
Why is this data in six tables. Move on after a learner can explain the current example or required action.

## Slide 5 — Why is this data in six tables

TEACHING PURPOSE
Why is this data in six tables

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Because one big sheet stores the same fact many times, and every copy is a chance to be wrong.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Why not one big sheet. Move on after a learner can explain the current example or required action.

## Slide 6 — Why not one big sheet

TEACHING PURPOSE
Why not one big sheet

CONNECT
Build on the preceding slide: Why is this data in six tables.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
What goes wrong with one big sheet. Move on after a learner can explain the current example or required action.

## Slide 7 — What goes wrong with one big sheet

TEACHING PURPOSE
What goes wrong with one big sheet

CONNECT
Build on the preceding slide: Why not one big sheet.

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
Primary key. Move on after a learner can explain the current example or required action.

## Slide 8 — Primary key

TEACHING PURPOSE
Primary key

CONNECT
Build on the preceding slide: What goes wrong with one big sheet.

LECTURER CUE
A column whose value is never repeated, so it identifies exactly one row. Every proper table has one.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Foreign key. Move on after a learner can explain the current example or required action.

## Slide 9 — Foreign key

TEACHING PURPOSE
Foreign key

CONNECT
Build on the preceding slide: Primary key.

LECTURER CUE
A column that holds another table's primary key. It is what connects the two tables.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
One-to-many. Move on after a learner can explain the current example or required action.

## Slide 10 — One-to-many

TEACHING PURPOSE
One-to-many

CONNECT
Build on the preceding slide: Foreign key.

LECTURER CUE
One row on one side matches several rows on the other. It is the commonest relationship in business data and the reason totals go wrong.

NEXT
The same business, two different grains. Move on after a learner can explain the current example or required action.

## Slide 11 — The same business, two different grains

TEACHING PURPOSE
The same business, two different grains

CONNECT
Build on the preceding slide: One-to-many.

LECTURER CUE
Left: one row is one order. Right: one row is one order line, so an order appears more than once. Both are real rows from the course data. The caption is the number to remember.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: The same business, two different grains.

LECTURER CUE
Ten minutes.

NEXT
Grain, keys, and what a join does. Move on after a learner can explain the current example or required action.

## Slide 13 — Grain, keys, and what a join does

TEACHING PURPOSE
Grain, keys, and what a join does

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
What a join does, and what an INNER JOIN quietly throws away. Move on after a learner can explain the current example or required action.

## Slide 14 — What a join does, and what an INNER JOIN quietly throws away

TEACHING PURPOSE
What a join does, and what an INNER JOIN quietly throws away

CONNECT
Build on the preceding slide: Grain, keys, and what a join does.

LECTURER CUE
Real counts from the course data. The INNER JOIN loses the 172 walk-in orders because they have no customer to match, and nothing in the output says so.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
The six tables, and how they connect. Move on after a learner can explain the current example or required action.

## Slide 15 — The six tables, and how they connect

TEACHING PURPOSE
The six tables, and how they connect

CONNECT
Build on the preceding slide: What a join does, and what an INNER JOIN quietly throws away.

LECTURER CUE
You will build exactly this in Power BI in session 14. Tonight you only need to see that the arrows all point the same way: many orders to one customer.

READ THE VISUAL
Start with the title and labels. Read one row or mark aloud, including its unit. Let a learner read a second one before discussing the pattern. Do not infer a numerical value from an unlabelled drawing.

NEXT
Tonight's lab has no SQL in it. Move on after a learner can explain the current example or required action.

## Slide 16 — Tonight's lab has no SQL in it

TEACHING PURPOSE
Tonight's lab has no SQL in it

CONNECT
Build on the preceding slide: The six tables, and how they connect.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Assuming one row means what you assume it means. Every wrong total later in this course comes from a grain nobody said out loud.. Move on after a learner can explain the current example or required action.

## Slide 17 — Assuming one row means what you assume it means. Every wrong total later in this course comes from a grain nobody said out loud.

TEACHING PURPOSE
Assuming one row means what you assume it means. Every wrong total later in this course comes from a grain nobody said out loud.

CONNECT
Build on the preceding slide: Tonight's lab has no SQL in it.

LECTURER CUE
Assuming one row means what you assume it means. Every wrong total later in this course comes from a grain nobody said out loud.

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
Build on the preceding slide: Assuming one row means what you assume it means. Every wrong total later in this course comes from a grain nobody said out loud..

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
One edit or many
One edit in the customers table. In a flat sheet, one edit per order that customer ever placed, and the ones you miss stay wrong and keep being summed.
B
Empty customer_id on 172 orders
No. It is walk-in trade: a real order with real revenue and no customer recorded. It becomes an error only if somebody joins to customers without noticing, which silently removes UGX 390,632,335 from the answer.
C
Row count after joining orders to lines
More. It is one-to-many, so each order appears once per line: 6,000 becomes 20,234. That is correct, and summing an order-level figure on that result is not.
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
Map the six tables by clicking. Move on after a learner can explain the current example or required action.

## Slide 20 — Map the six tables by clicking

TEACHING PURPOSE
Map the six tables by clicking

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
No SQL tonight. In DB Browser's Browse Data tab, work through all six tables and fill in the sheet: grain, primary key, foreign keys. Then draw the six boxes and the arrows between them on paper. Drawing it by hand is what makes it stick.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 21 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Map the six tables by clicking.

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
Take one report you receive at work and work out how many tables it was probably built from. Name them and the key each would join on. You will be right more often than you expect.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Say the grain out loud, every time. Move on after a learner can explain the current example or required action.

## Slide 23 — Say the grain out loud, every time

TEACHING PURPOSE
Say the grain out loud, every time

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Nearly every wrong total in the rest of this course comes from a grain nobody stated. Two sessions with no code buys you that habit, and it is the cheapest thing you will learn here.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

