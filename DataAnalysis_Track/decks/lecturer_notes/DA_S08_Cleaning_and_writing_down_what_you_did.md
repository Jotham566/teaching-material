# DA S08 Cleaning and writing down what you did

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Cleaning, and writing down what you did

TEACHING PURPOSE
Cleaning, and writing down what you did

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Cleaning, and writing down what you did.

LECTURER CUE
Tonight is session 8 of fifteen.

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
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
You cleaned the data and got a number.. Move on after a learner can explain the current example or required action.

## Slide 5 — You cleaned the data and got a number.

TEACHING PURPOSE
You cleaned the data and got a number.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
Only if you wrote down what you changed. Cleaning is a series of decisions, and a decision nobody recorded is a number nobody can reproduce.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Seven defects, found and fixed. Move on after a learner can explain the current example or required action.

## Slide 6 — Seven defects, found and fixed

TEACHING PURPOSE
Seven defects, found and fixed

CONNECT
Build on the preceding slide: You cleaned the data and got a number..

EXPLAIN IN ORDINARY WORDS
A category is a label, not an amount. Indicator columns record whether a row belongs to each category, usually with 0 or 1. Fit the encoding on training data and reuse it.

CHECK AND EXPECTED ANSWER
Does assigning red=1 and blue=2 mean blue is twice red? No, those are labels.

IF LEARNERS ARE STUCK
Make two rows and two category columns by hand before showing the encoder.

NEXT
The seven defects in tonight's file, and what each one costs. Move on after a learner can explain the current example or required action.

## Slide 7 — The seven defects in tonight's file, and what each one costs

TEACHING PURPOSE
The seven defects in tonight's file, and what each one costs

CONNECT
Build on the preceding slide: Seven defects, found and fixed.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
A cleaning log. Move on after a learner can explain the current example or required action.

## Slide 8 — A cleaning log

TEACHING PURPOSE
A cleaning log

CONNECT
Build on the preceding slide: The seven defects in tonight's file, and what each one costs.

LECTURER CUE
A table recording rows in, rows out, what changed and why, written as you work rather than afterwards.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Reconciliation. Move on after a learner can explain the current example or required action.

## Slide 9 — Reconciliation

TEACHING PURPOSE
Reconciliation

CONNECT
Build on the preceding slide: A cleaning log.

LECTURER CUE
Getting the same number two different ways and chasing every difference until you can name it.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Residual. Move on after a learner can explain the current example or required action.

## Slide 10 — Residual

TEACHING PURPOSE
Residual

CONNECT
Build on the preceding slide: Reconciliation.

LECTURER CUE
The difference left after you have explained everything you can. Naming it is part of the job.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Duplicates, and the returns convention. Move on after a learner can explain the current example or required action.

## Slide 11 — Duplicates, and the returns convention

TEACHING PURPOSE
Duplicates, and the returns convention

CONNECT
Build on the preceding slide: Residual.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Duplicates, and the returns convention.

LECTURER CUE
Ten minutes.

NEXT
The decision, the log, and the reconciliation. Move on after a learner can explain the current example or required action.

## Slide 13 — The decision, the log, and the reconciliation

TEACHING PURPOSE
The decision, the log, and the reconciliation

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
The defect nothing in the file tells you about. Move on after a learner can explain the current example or required action.

## Slide 14 — The defect nothing in the file tells you about

TEACHING PURPOSE
The defect nothing in the file tells you about

CONNECT
Build on the preceding slide: The decision, the log, and the reconciliation.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

NEXT
Two date formats in one column. Move on after a learner can explain the current example or required action.

## Slide 15 — Two date formats in one column

TEACHING PURPOSE
Two date formats in one column

CONNECT
Build on the preceding slide: The defect nothing in the file tells you about.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
The reconciliation does not come out exact, and that is the lesson. Move on after a learner can explain the current example or required action.

## Slide 16 — The reconciliation does not come out exact, and that is the lesson

TEACHING PURPOSE
The reconciliation does not come out exact, and that is the lesson

CONNECT
Build on the preceding slide: Two date formats in one column.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Cleaning until the number looks right. The log exists to make that visible, including to yourself.. Move on after a learner can explain the current example or required action.

## Slide 17 — Cleaning until the number looks right. The log exists to make that visible, including to yourself.

TEACHING PURPOSE
Cleaning until the number looks right. The log exists to make that visible, including to yourself.

CONNECT
Build on the preceding slide: The reconciliation does not come out exact, and that is the lesson.

LECTURER CUE
Cleaning until the number looks right. The log exists to make that visible, including to yourself.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 18 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Cleaning until the number looks right. The log exists to make that visible, including to yourself..

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
When a duplicate is not an error
When the grain allows it: two identical payments on one day are two real payments. On an order line it is an error, because the same product twice on one order would be one line with quantity 2. The grain decides, which is why session 1 spent an hour on it.
B
Finding a currency defect unaided
Ask what a price should look like, then check min and max per category. A category whose prices are a thousandth of everything else is not a cheap category. Domain sense is the detector; there is no error message.
C
Why a missing customer id is a decision
Because both answers are defensible and they give different numbers. Dropping those orders loses UGX 390,632,335; keeping them means every per-customer analysis has a gap you must state. What is not defensible is doing either one silently.
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
Clean it, log it, reconcile it. Move on after a learner can explain the current example or required action.

## Slide 20 — Clean it, log it, reconcile it

TEACHING PURPOSE
Clean it, log it, reconcile it

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
From the raw CSVs to a revenue figure you can defend, keeping the log as you go rather than writing it afterwards. The log is marked as heavily as the number.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 21 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Clean it, log it, reconcile it.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 22 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Clean your own file, or the retail file, with a log. State one decision you are not sure about and why. Uncertainty written down is worth more than a confident wrong number.

NEXT
A number nobody can reproduce is not a result. Move on after a learner can explain the current example or required action.

## Slide 23 — A number nobody can reproduce is not a result

TEACHING PURPOSE
A number nobody can reproduce is not a result

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
In six months the person who cannot reproduce it will be you. The log costs five minutes while you work and saves an afternoon later, which is the best trade available in this course.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

