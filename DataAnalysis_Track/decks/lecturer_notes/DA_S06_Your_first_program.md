# DA S06 Your first program

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — Your first program

TEACHING PURPOSE
Your first program

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: Your first program.

LECTURER CUE
Tonight is session 6 of fifteen.

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
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

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

NEXT
You have never programmed.. Move on after a learner can explain the current example or required action.

## Slide 5 — You have never programmed.

TEACHING PURPOSE
You have never programmed.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
About ninety minutes. Tonight you load a real file and print how many rows it has.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
You already write code. Move on after a learner can explain the current example or required action.

## Slide 6 — You already write code

TEACHING PURPOSE
You already write code

CONNECT
Build on the preceding slide: You have never programmed..

DELIVER THIS SLIDE
Read the stated purpose, then point to the named example or action on the slide. Ask learners to describe what they will do before moving on. For a break slide, announce the return time; for a section divider, name the next concrete task.

NEXT
A spreadsheet formula, with the parts named. Move on after a learner can explain the current example or required action.

## Slide 7 — A spreadsheet formula, with the parts named

TEACHING PURPOSE
A spreadsheet formula, with the parts named

CONNECT
Build on the preceding slide: You already write code.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Variable. Move on after a learner can explain the current example or required action.

## Slide 8 — Variable

TEACHING PURPOSE
Variable

CONNECT
Build on the preceding slide: A spreadsheet formula, with the parts named.

LECTURER CUE
A name that holds a value, so you can use it again without retyping it. You choose the name.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
Function. Move on after a learner can explain the current example or required action.

## Slide 9 — Function

TEACHING PURPOSE
Function

CONNECT
Build on the preceding slide: Variable.

LECTURER CUE
A named instruction that takes inputs, does something, and gives back a result. You use other people's and you write your own.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Library. Move on after a learner can explain the current example or required action.

## Slide 10 — Library

TEACHING PURPOSE
Library

CONNECT
Build on the preceding slide: Function.

LECTURER CUE
Somebody else's functions, loaded when you need them. You will use one library, pandas, for almost everything in weeks three and four.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
Traceback. Move on after a learner can explain the current example or required action.

## Slide 11 — Traceback

TEACHING PURPOSE
Traceback

CONNECT
Build on the preceding slide: Library.

LECTURER CUE
The error message Python prints when something goes wrong. It is long, it looks alarming, and the LAST line is the one that names the problem.

NEXT
Zero-based counting. Move on after a learner can explain the current example or required action.

## Slide 12 — Zero-based counting

TEACHING PURPOSE
Zero-based counting

CONNECT
Build on the preceding slide: Traceback.

LECTURER CUE
Python counts from 0, so the first row is row 0 and the first item of a list is item 0.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Everything in the left half, in fourteen lines. Move on after a learner can explain the current example or required action.

## Slide 13 — Everything in the left half, in fourteen lines

TEACHING PURPOSE
Everything in the left half, in fourteen lines

CONNECT
Build on the preceding slide: Zero-based counting.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 14 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Everything in the left half, in fourteen lines.

LECTURER CUE
Ten minutes.

NEXT
Your first DataFrame. Move on after a learner can explain the current example or required action.

## Slide 15 — Your first DataFrame

TEACHING PURPOSE
Your first DataFrame

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
Make three errors on purpose. Move on after a learner can explain the current example or required action.

## Slide 16 — Make three errors on purpose

TEACHING PURPOSE
Make three errors on purpose

CONNECT
Build on the preceding slide: Your first DataFrame.

EXPLAIN IN ORDINARY WORDS
A CSV is a text table. The header supplies column names. With csv.DictReader, values start as text, even if they look like numbers. A path tells Python where the file is.

CHECK AND EXPECTED ANSWER
Can "2.5" from csv.DictReader be added as a number without conversion? No; convert valid numeric text first.

IF LEARNERS ARE STUCK
Show the file in the runtime folder and compare its exact filename, case and column headers. Upload data again after a fresh Colab runtime.

NEXT
Your first DataFrame. Move on after a learner can explain the current example or required action.

## Slide 17 — Your first DataFrame

TEACHING PURPOSE
Your first DataFrame

CONNECT
Build on the preceding slide: Make three errors on purpose.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Copying code you cannot read. It works, you learn nothing, and the first time it breaks you are stuck. Type it.. Move on after a learner can explain the current example or required action.

## Slide 18 — Copying code you cannot read. It works, you learn nothing, and the first time it breaks you are stuck. Type it.

TEACHING PURPOSE
Copying code you cannot read. It works, you learn nothing, and the first time it breaks you are stuck. Type it.

CONNECT
Build on the preceding slide: Your first DataFrame.

LECTURER CUE
Copying code you cannot read. It works, you learn nothing, and the first time it breaks you are stuck. Type it.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 19 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Copying code you cannot read. It works, you learn nothing, and the first time it breaks you are stuck. Type it..

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
A variable, in your own words
A name that holds a value so you can use it again. Like naming a cell, except you pick the name and it can say what it means.
B
NameError on a name you thought you had
Read it literally: that name does not exist. Nine times in ten it is a typo, or a cell you have not run yet. Scroll up, find where you meant to create it, and run that cell.
C
Why regions[4] fails
Because counting starts at 0, so four items are numbered 0, 1, 2 and 3. There is no item 4. This is the one real difference from Excel and it catches everybody once.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 20 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
Type it yourself, from a blank notebook. Move on after a learner can explain the current example or required action.

## Slide 21 — Type it yourself, from a blank notebook

TEACHING PURPOSE
Type it yourself, from a blank notebook

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Nothing is pasted tonight. Open an empty notebook and type every line. It is slower and it is the only version that teaches you anything.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 22 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Type it yourself, from a blank notebook.

EXPLAIN IN ORDINARY WORDS
A DataFrame is a labelled table. A Series is a single labelled sequence, often one column. A dtype describes stored values, but the import may infer something unsuitable.

CHECK AND EXPECTED ANSWER
Does a price that looks numeric prove the column is numeric? No. Inspect its dtype and troublesome values before conversion.

IF LEARNERS ARE STUCK
Use head, shape and dtypes to locate the table, count rows/columns and inspect storage. Check units and missing values before calculating.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 23 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Retype tonight's notebook from scratch without looking. It takes fifteen minutes and it is worth more than an hour of reading.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
You wrote a program tonight. Move on after a learner can explain the current example or required action.

## Slide 24 — You wrote a program tonight

TEACHING PURPOSE
You wrote a program tonight

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
It loaded a real file of 6,000 rows and told you something true about it. The rest of this course is more of the same, in bigger steps.

