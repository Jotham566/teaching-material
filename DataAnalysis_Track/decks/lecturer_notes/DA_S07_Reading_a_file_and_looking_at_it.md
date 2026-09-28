# DA S07 Reading a file and looking at it

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Reading a file, and looking at it

TEACHING PURPOSE
Reading a file, and looking at it

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Reading a file, and looking at it.

LECTURER CUE
Tonight is session 7 of fifteen.

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

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

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
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Somebody sends you a file you have never seen.. Move on after a learner can explain the current example or required action.

## Slide 5 — Somebody sends you a file you have never seen.

TEACHING PURPOSE
Somebody sends you a file you have never seen.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
The same six commands, in the same order, every time. It is the cheapest habit in this work.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

NEXT
Six commands, on any file you have never seen. Move on after a learner can explain the current example or required action.

## Slide 6 — Six commands, on any file you have never seen

TEACHING PURPOSE
Six commands, on any file you have never seen

CONNECT
Build on the preceding slide: Somebody sends you a file you have never seen..

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Series. Move on after a learner can explain the current example or required action.

## Slide 7 — Series

TEACHING PURPOSE
Series

CONNECT
Build on the preceding slide: Six commands, on any file you have never seen.

LECTURER CUE
One column of a DataFrame, on its own. Selecting a single column gives you one of these rather than a table.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
dtype. Move on after a learner can explain the current example or required action.

## Slide 8 — dtype

TEACHING PURPOSE
dtype

CONNECT
Build on the preceding slide: Series.

LECTURER CUE
The type pandas decided a column has when it read the file. You did not choose it and it is not always right.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Missing value. Move on after a learner can explain the current example or required action.

## Slide 9 — Missing value

TEACHING PURPOSE
Missing value

CONNECT
Build on the preceding slide: dtype.

LECTURER CUE
A cell with nothing recorded. pandas shows it as NaN, which stands for not a number and appears in text columns too.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
The six commands. Learn the order, not the words.. Move on after a learner can explain the current example or required action.

## Slide 10 — The six commands. Learn the order, not the words.

TEACHING PURPOSE
The six commands. Learn the order, not the words.

CONNECT
Build on the preceding slide: Missing value.

EXPLAIN IN ORDINARY WORDS
Cross-validation repeats training and validation on different partitions. Each fold gets a newly fitted model and preprocessing. Variation across fold scores shows sensitivity to the partition.

CHECK AND EXPECTED ANSWER
May preprocessing learn from all rows before the folds? No, that would give each validation fold information from outside its training portion.

IF LEARNERS ARE STUCK
Draw three small partitions and label who learns and who is evaluated. Fold spread is not automatically a confidence interval.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 11 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: The six commands. Learn the order, not the words..

LECTURER CUE
Ten minutes.

NEXT
Selecting, filtering, and the type that lies. Move on after a learner can explain the current example or required action.

## Slide 12 — Selecting, filtering, and the type that lies

TEACHING PURPOSE
Selecting, filtering, and the type that lies

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Selecting and filtering, which is autofilter written down. Move on after a learner can explain the current example or required action.

## Slide 13 — Selecting and filtering, which is autofilter written down

TEACHING PURPOSE
Selecting and filtering, which is autofilter written down

CONNECT
Build on the preceding slide: Selecting, filtering, and the type that lies.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
The type that lies. Move on after a learner can explain the current example or required action.

## Slide 14 — The type that lies

TEACHING PURPOSE
The type that lies

CONNECT
Build on the preceding slide: Selecting and filtering, which is autofilter written down.

EXPLAIN IN ORDINARY WORDS
Grain means what one row represents. A key identifies a row; a primary key may use more than one column. A join matches keys, and multiple matches can multiply rows.

CHECK AND EXPECTED ANSWER
One order has two lines. After joining orders to lines, how many rows for it? Two. Summing a repeated order-level total would double-count.

IF LEARNERS ARE STUCK
Write one example row from each table. Circle keys and trace each match. Aggregate to the intended grain and check counts and totals.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Profiling a file you have never seen. Move on after a learner can explain the current example or required action.

## Slide 15 — Profiling a file you have never seen

TEACHING PURPOSE
Profiling a file you have never seen

CONNECT
Build on the preceding slide: The type that lies.

LECTURER CUE
The routine in a fixed order. Two minutes, and afterwards you can say what the file can and cannot answer.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
A large workbook to inspect with pandas. Move on after a learner can explain the current example or required action.

## Slide 16 — A large workbook to inspect with pandas

TEACHING PURPOSE
A large workbook to inspect with pandas

CONNECT
Build on the preceding slide: Profiling a file you have never seen.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Reading a file and trusting the types. A column of numbers arriving as text is the commonest cause of a wrong answer in pandas, and nothing raises an error.. Move on after a learner can explain the current example or required action.

## Slide 17 — Reading a file and trusting the types. A column of numbers arriving as text is the commonest cause of a wrong answer in pandas, and nothing raises an error.

TEACHING PURPOSE
Reading a file and trusting the types. A column of numbers arriving as text is the commonest cause of a wrong answer in pandas, and nothing raises an error.

CONNECT
Build on the preceding slide: A large workbook to inspect with pandas.

LECTURER CUE
Reading a file and trusting the types. A column of numbers arriving as text is the commonest cause of a wrong answer in pandas, and nothing raises an error.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 18 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Reading a file and trusting the types. A column of numbers arriving as text is the commonest cause of a wrong answer in pandas, and nothing raises an error..

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
A price column with dtype object
Something in it is not a number: a comma, a currency symbol, a blank, or a word. It does not tell you which or how many, and value_counts() on the odd values is how you find out.
B
A mean customer_id
It is an identifier that happens to be stored as a number. describe() computes statistics on anything numeric and cannot tell an identifier from a measurement. The judgement is yours.
C
Why the missing-value count is not optional
Because a blank is not a zero, and every count, average and join downstream behaves differently depending on how many there are. Here it is 172 rows worth UGX 390,632,335.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

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

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Profile Online Retail II. Move on after a learner can explain the current example or required action.

## Slide 20 — Profile Online Retail II

TEACHING PURPOSE
Profile Online Retail II

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Download it, open it in pandas, and produce the one-page profile. You are not cleaning it tonight. The goal is to be able to say, in three sentences, what the file is a record of and what it cannot tell you.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

WORKBOOK CLARIFICATION
Do not say an Excel workbook cannot open solely because the combined row count exceeds one worksheet limit. Check its sheet names. pandas.read_excel uses the first sheet by default; sheet_name=None returns a dictionary of all sheets. Select or combine compatible sheets deliberately and check the resulting date range. Source: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 21 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Profile Online Retail II.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 22 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Profile a file from your own work, or a second sheet of the retail file, and write the three sentences. The sentences are harder than the code and they are the point.

NEXT
Look before you compute. Move on after a learner can explain the current example or required action.

## Slide 23 — Look before you compute

TEACHING PURPOSE
Look before you compute

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Six commands, two minutes. Every hour lost in this work is lost to an assumption about a file that nobody checked, and the check is cheaper than the assumption every single time.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

