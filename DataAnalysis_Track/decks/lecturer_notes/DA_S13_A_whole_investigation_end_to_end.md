# DA S13 A whole investigation end to end

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — A whole investigation, end to end

TEACHING PURPOSE
A whole investigation, end to end

LECTURER CUE
Start on time.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Where tonight sits. Move on after a learner can explain the current example or required action.

## Slide 2 — Where tonight sits

TEACHING PURPOSE
Where tonight sits

CONNECT
Build on the preceding slide: A whole investigation, end to end.

LECTURER CUE
Tonight is session 13 of fifteen.

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
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

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
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
You have a file you have never seen and three hours.. Move on after a learner can explain the current example or required action.

## Slide 5 — You have a file you have never seen and three hours.

TEACHING PURPOSE
You have a file you have never seen and three hours.

CONNECT
Build on the preceding slide: By the end of tonight you can….

LECTURER CUE
In the same place every time. The routine is what stops an investigation becoming forty cells and no conclusion.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
The routine, in a fixed order. Move on after a learner can explain the current example or required action.

## Slide 6 — The routine, in a fixed order

TEACHING PURPOSE
The routine, in a fixed order

CONNECT
Build on the preceding slide: You have a file you have never seen and three hours..

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
The routine. Same order, every dataset, every time.. Move on after a learner can explain the current example or required action.

## Slide 7 — The routine. Same order, every dataset, every time.

TEACHING PURPOSE
The routine. Same order, every dataset, every time.

CONNECT
Build on the preceding slide: The routine, in a fixed order.

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

NEXT
A finding. Move on after a learner can explain the current example or required action.

## Slide 8 — A finding

TEACHING PURPOSE
A finding

CONNECT
Build on the preceding slide: The routine. Same order, every dataset, every time..

LECTURER CUE
A sentence with a number in it that somebody could act on or dispute. It is about the business, not about the data.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
An observation. Move on after a learner can explain the current example or required action.

## Slide 9 — An observation

TEACHING PURPOSE
An observation

CONNECT
Build on the preceding slide: A finding.

LECTURER CUE
Something true about the data rather than about the business. It belongs in your notebook and not in your findings.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
A stated limitation. Move on after a learner can explain the current example or required action.

## Slide 10 — A stated limitation

TEACHING PURPOSE
A stated limitation

CONNECT
Build on the preceding slide: An observation.

LECTURER CUE
The sentence beside a finding saying where it stops being reliable. Beside it, not in a footnote, because that is where the person acting on it will read.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Leakage. Move on after a learner can explain the current example or required action.

## Slide 11 — Leakage

TEACHING PURPOSE
Leakage

CONNECT
Build on the preceding slide: A stated limitation.

LECTURER CUE
Using a column you would not have had at decision time, which makes the answer look far better than it is.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 12 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: Leakage.

LECTURER CUE
Ten minutes.

NEXT
From eleven observations to five findings. Move on after a learner can explain the current example or required action.

## Slide 13 — From eleven observations to five findings

TEACHING PURPOSE
From eleven observations to five findings

CONNECT
Build on the preceding slide: Break.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Turning eleven observations into five findings. Move on after a learner can explain the current example or required action.

## Slide 14 — Turning eleven observations into five findings

TEACHING PURPOSE
Turning eleven observations into five findings

CONNECT
Build on the preceding slide: From eleven observations to five findings.

LECTURER CUE
An investigation produces far more observations than findings. Choosing between them is part of the work.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

TYPE NUANCE
An object dtype alone does not prove that a column contains bad numeric values; it can hold Python objects, including numbers. Inspect values and conversion results. Missing values may display as NaN, None, NaT or pandas NA depending on dtype.

NEXT
Choose your sector dataset tonight. Move on after a learner can explain the current example or required action.

## Slide 15 — Choose your sector dataset tonight

TEACHING PURPOSE
Choose your sector dataset tonight

CONNECT
Build on the preceding slide: Turning eleven observations into five findings.

EXPLAIN IN ORDINARY WORDS
Grouping puts rows sharing a key into buckets, then computes a result for each bucket. WHERE filters rows before SQL grouping; HAVING filters grouped results.

CHECK AND EXPECTED ANSWER
Which condition keeps only groups with more than five rows? HAVING COUNT(*) > 5.

IF LEARNERS ARE STUCK
Draw two buckets and count by hand. Name the intended output grain before writing the aggregation.

NEXT
A notebook with forty cells and no conclusion. The routine exists to stop exactly that.. Move on after a learner can explain the current example or required action.

## Slide 16 — A notebook with forty cells and no conclusion. The routine exists to stop exactly that.

TEACHING PURPOSE
A notebook with forty cells and no conclusion. The routine exists to stop exactly that.

CONNECT
Build on the preceding slide: Choose your sector dataset tonight.

LECTURER CUE
A notebook with forty cells and no conclusion. The routine exists to stop exactly that.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 17 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: A notebook with forty cells and no conclusion. The routine exists to stop exactly that..

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Finding against observation
A finding is about the business, has a number in it, and somebody could act on it or dispute it. An observation is about the data. Both belong in the notebook; only findings belong in the summary.
B
An investigation with no surprises
No. Confirming what the room believed, with numbers attached, converts an assumption into something checkable. What IS a failure is not knowing which of the two you produced.
C
Why the limitation sits beside the finding
Because that is where the person acting on it reads. A limitation at the end of a document is a limitation nobody saw, and you will still be the one defending the number.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 18 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Run the routine on your sector dataset. Move on after a learner can explain the current example or required action.

## Slide 19 — Run the routine on your sector dataset

TEACHING PURPOSE
Run the routine on your sector dataset

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
This is the sector assessment, worth 30%. Six questions in order, then five findings. Marked on the findings and the limitations beside them, not on the code.

EXPLAIN IN ORDINARY WORDS
Mean is total divided by count. Median is the middle of sorted values. A percentile locates a position in that ordered distribution; interpolation conventions can differ. Match the summary to the question.

CHECK AND EXPECTED ANSWER
For [2,3,4,5,100], median=4 and mean=22.8. The large value pulls the mean up.

IF LEARNERS ARE STUCK
Sort five values by hand. A skewed distribution does not make the mean wrong if the question concerns totals or expected cost.

NEXT
What you can do now. Move on after a learner can explain the current example or required action.

## Slide 20 — What you can do now

TEACHING PURPOSE
What you can do now

CONNECT
Build on the preceding slide: Run the routine on your sector dataset.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
Before the next session. Move on after a learner can explain the current example or required action.

## Slide 21 — Before the next session

TEACHING PURPOSE
Before the next session

CONNECT
Build on the preceding slide: What you can do now.

LECTURER CUE
Finish and submit the investigation: half a page of findings plus the notebook behind it.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

NEXT
A routine beats talent under time pressure. Move on after a learner can explain the current example or required action.

## Slide 22 — A routine beats talent under time pressure

TEACHING PURPOSE
A routine beats talent under time pressure

CONNECT
Build on the preceding slide: Before the next session.

LECTURER CUE
Every analyst you would want to hire has one. It is what lets them open an unfamiliar file at nine and say something defensible by eleven, which is the actual job.

