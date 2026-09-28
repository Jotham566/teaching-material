# CML3112 Week01 Design Infrastructure

Private lecturer companion. These same notes are embedded in the PowerPoint. Use Presenter View; keep the student display on slides only.

## Slide 1 — AI, machine learning

TEACHING PURPOSE
AI, machine learning

LECTURER CUE
Today runs entirely on paper. You will not touch a computer, so nothing you do this session depends on owning a laptop or having a connection. By the end you will have answered a real engineering question from twelve rows of a real dataset with a pencil, and measured how wrong you were.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Jotham Martin Wambi. Move on after a learner can explain the current example or required action.

## Slide 2 — Jotham Martin Wambi

TEACHING PURPOSE
Jotham Martin Wambi

CONNECT
Build on the preceding slide: AI, machine learning.

LECTURER CUE
A short introduction, and there is a reason for it beyond courtesy.
First, so that you know what you can ask me for. The work on the right is where my experience actually is: sensor data and predictive maintenance, language models over documents, and getting models into something a colleague can use. If your project heads in one of those directions I can help you in detail. If it heads somewhere I know less well, I will tell you that rather than guess.
Second, because of the route rather than the titles. I read economics and information technology as undergraduate degrees, and my first seven years of work were in banking, tax and product management, none of which involved building a model. Nobody starts where this field expects them to start, and the engineering degree you are already halfway through is a better foundation for machine learning than most computing degrees, for reasons we come to in the roadmap segment.
Third, so the claims in this course are checkable. Where I tell you a technique behaves a certain way, it is usually because I have watched it fail somewhere first.
The contact details are real. Use them.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
By the end of today you can…. Move on after a learner can explain the current example or required action.

## Slide 3 — By the end of today you can…

TEACHING PURPOSE
By the end of today you can…

CONNECT
Build on the preceding slide: Jotham Martin Wambi.

LECTURER CUE
Seven objectives, and they are the whole session. Nothing is hidden behind them and there is no reading list you are expected to have done. Mark yourself against each one at the end of the session; whatever you cannot claim is what to revise before Week 2.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
How every session this semester is shaped. Move on after a learner can explain the current example or required action.

## Slide 4 — How every session this semester is shaped

TEACHING PURPOSE
How every session this semester is shaped

CONNECT
Build on the preceding slide: By the end of today you can….

LECTURER CUE
Every session this semester has the same shape: eleven segments across three hours, with no block of talking longer than 25 minutes and roughly half the time spent working rather than listening. That is why attendance matters more here than on a lecture course — the practical and challenge segments cannot be read off a deck afterwards. There is a 10-minute break at the midpoint.

NEXT
Where this semester goes. Move on after a learner can explain the current example or required action.

## Slide 5 — Where this semester goes

TEACHING PURPOSE
Where this semester goes

CONNECT
Build on the preceding slide: How every session this semester is shaped.

LECTURER CUE
Fifteen weeks. Weeks 7 and 14 are practical tests where you are given data you have never seen and asked what you make of it, and the project runs from Week 9 to the last session. There is nothing to memorise in this course, which surprises most students who arrive expecting to revise definitions.

NEXT
What you will be able to say by December. Move on after a learner can explain the current example or required action.

## Slide 6 — What you will be able to say by December

TEACHING PURPOSE
What you will be able to say by December

CONNECT
Build on the preceding slide: Where this semester goes.

LECTURER CUE
Six steps, from knowing what a dataset is to saying 'here is a model I built and here is how I know it works'. Most of you cannot do step two today and all of you can reach step six by December. The students who get there are the ones who do the weekly deliverable every week, and the difference is visible by about Week 6.

NEXT
Welcome, and how this course works. Move on after a learner can explain the current example or required action.

## Slide 7 — Welcome, and how this course works

TEACHING PURPOSE
Welcome, and how this course works

CONNECT
Build on the preceding slide: What you will be able to say by December.

LECTURER CUE
Fifteen minutes on how the course works: the promise, the assessment, and what is expected on both sides. Everything after this segment is engineering.

NEXT
How you are assessed. Move on after a learner can explain the current example or required action.

## Slide 8 — How you are assessed

TEACHING PURPOSE
How you are assessed

CONNECT
Build on the preceding slide: Welcome, and how this course works.

LECTURER CUE
Two details the figure does not carry. Every teaching session ends with a five-minute quiz of five questions, taken on your phone by QR code, auto-marked, and you have your score before you leave the room. There are twelve of them and the best ten count, one per cent each, so missing two costs you nothing and there are no resits to arrange. The two practical tests run offline on lab machines with no internet and no AI assistants. AI tools are permitted and taught in the coursework provided you declare what you used, because the mark follows what you can explain.

NEXT
What I expect, and what you can expect back. Move on after a learner can explain the current example or required action.

## Slide 9 — What I expect, and what you can expect back

TEACHING PURPOSE
What I expect, and what you can expect back

CONNECT
Build on the preceding slide: How you are assessed.

LECTURER CUE
The 'ask well' item is the one that changes how much you get out of the semester. Bring the error message, what you already tried, and what you expected to happen; assembling those three things solves the problem outright often enough to be worth the effort every time. If you are stuck for more than five minutes in a practical, put your hand up rather than sitting quietly.

NEXT
The whole field, start to finish. Move on after a learner can explain the current example or required action.

## Slide 10 — The whole field, start to finish

TEACHING PURPOSE
The whole field, start to finish

CONNECT
Build on the preceding slide: What I expect, and what you can expect back.

LECTURER CUE
This segment hands you the map of the field before any of it is taught, so that every later week has somewhere to sit rather than arriving from nowhere. The structure follows the public roadmap.sh Machine Learning roadmap, which is the map the profession itself uses, so you can check this course against something written outside this room.

NEXT
The machine learning roadmap. Move on after a learner can explain the current example or required action.

## Slide 11 — The machine learning roadmap

TEACHING PURPOSE
The machine learning roadmap

CONNECT
Build on the preceding slide: The whole field, start to finish.

LECTURER CUE
Fifteen stages, from Python to transformers. By December you will have covered stages 1 to 9. Most of the individual terms on the figure mean nothing to you today and that is expected — what to take from it is the shape of the field and where this course stops. The interactive version is at roadmap.sh/machine-learning, and it is worth an evening of clicking around.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Stage 2 is the one that matters to you. Move on after a learner can explain the current example or required action.

## Slide 12 — Stage 2 is the one that matters to you

TEACHING PURPOSE
Stage 2 is the one that matters to you

CONNECT
Build on the preceding slide: The machine learning roadmap.

LECTURER CUE
The mathematics stage — calculus, linear algebra, statistics, probability — is the one most people entering this field find hardest, and you did it in Years 1 and 2. What you are missing is stages 1 and 3, Python and the data libraries, which Weeks 2 to 6 cover in five weeks of work. The expensive prerequisite is already behind you.

EXPLAIN IN ORDINARY WORDS
A probability-like score and a class decision are different outputs. A threshold turns a score into an action. Lowering a warning threshold usually raises both detections and false alarms.

CHECK AND EXPECTED ANSWER
At a rule of score >= 0.5, what happens at 0.5? It is positive. With > 0.5 it would not be.

IF LEARNERS ARE STUCK
Mark three scores below, at and above the boundary. Do not promise the score is well calibrated without checking.

NEXT
Where this course sits, honestly. Move on after a learner can explain the current example or required action.

## Slide 13 — Where this course sits, honestly

TEACHING PURPOSE
Where this course sits, honestly

CONNECT
Build on the preceding slide: Stage 2 is the one that matters to you.

LECTURER CUE
The grey stages sit outside this course: reinforcement learning, full MLOps and most of the advanced language-model material. If you want to go after them later, roadmap.sh publishes separate roadmaps for the AI engineer, the data scientist, MLOps and AI agents, and any of the four is a reasonable next step after December.

NEXT
Four jobs this field splits into. Move on after a learner can explain the current example or required action.

## Slide 14 — Four jobs this field splits into

TEACHING PURPOSE
Four jobs this field splits into

CONNECT
Build on the preceding slide: Where this course sits, honestly.

LECTURER CUE
Four different roadmaps and four different careers. This course points at the first one, applied inside your own engineering discipline. A computer science graduate will beat you at general machine learning, and that contest is avoidable: a civil engineer who can model concrete strength, or a mining engineer who can predict concentrate quality, is competing in a much smaller field.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
What this course is actually about. Move on after a learner can explain the current example or required action.

## Slide 15 — What this course is actually about

TEACHING PURPOSE
What this course is actually about

CONNECT
Build on the preceding slide: Four jobs this field splits into.

LECTURER CUE
Three words — artificial intelligence, machine learning, data science — get used interchangeably in job adverts, papers and vendor brochures. Fifteen minutes here is what lets you read those documents without being misled by them.

NEXT
The words, and how they nest. Move on after a learner can explain the current example or required action.

## Slide 16 — The words, and how they nest

TEACHING PURPOSE
The words, and how they nest

CONNECT
Build on the preceding slide: What this course is actually about.

LECTURER CUE
Each term is contained by the one before it. Data science is the odd one out: it overlaps all of them and is contained by none, because it is the craft of getting an answer out of data at all — finding it, cleaning it, questioning it, presenting it. Most of your semester goes into the data science ring, and the modelling turns out to be the small part.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Artificial intelligence. Move on after a learner can explain the current example or required action.

## Slide 17 — Artificial intelligence

TEACHING PURPOSE
Artificial intelligence

CONNECT
Build on the preceding slide: The words, and how they nest.

LECTURER CUE
A thermostat follows one fixed rule and has no capacity to do better, which puts it outside the definition. A spam filter that improves as it sees more mail sits inside it. Whether any of this is 'really' intelligent is a genuine open question in the field; here the word is a label for an area of work.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Machine learning. Move on after a learner can explain the current example or required action.

## Slide 18 — Machine learning

TEACHING PURPOSE
Machine learning

CONNECT
Build on the preceding slide: Artificial intelligence.

LECTURER CUE
This is the definition the rest of the course rests on. Note the last step of the example: the computer infers a relationship and you then decide whether to trust it. That step is the easy one to skip, and Weeks 10 to 14 are entirely about it.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Data science. Move on after a learner can explain the current example or required action.

## Slide 19 — Data science

TEACHING PURPOSE
Data science

CONNECT
Build on the preceding slide: Machine learning.

LECTURER CUE
In industry the split is roughly eighty per cent getting data into a usable state and twenty per cent modelling. An engineer with clean data beats a better algorithm with dirty data. The missing-assay example on this slide is a real Week 6 exercise: you will be handed records with a large part of one column absent and asked whether they are missing at random and what that does to your conclusion.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Two ways to make a computer decide. Move on after a learner can explain the current example or required action.

## Slide 20 — Two ways to make a computer decide

TEACHING PURPOSE
Two ways to make a computer decide

CONNECT
Build on the preceding slide: Data science.

LECTURER CUE
The core teaching segment of the session: the difference between writing a rule and inferring one from examples, plus the vocabulary for talking about a table of data. Everything from Week 5 onwards assumes both.

NEXT
"Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?". Move on after a learner can explain the current example or required action.

## Slide 21 — "Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?"

TEACHING PURPOSE
"Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?"

CONNECT
Build on the preceding slide: Two ways to make a computer decide.

LECTURER CUE
Sit with the question before any answer arrives. Two honest first reactions are 'you cannot' and 'there must be a formula somewhere', and both are useful. The hands-on prediction exercise shows what a third answer looks like.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Traditional programming, and machine learning. Move on after a learner can explain the current example or required action.

## Slide 22 — Traditional programming, and machine learning

TEACHING PURPOSE
Traditional programming, and machine learning

CONNECT
Build on the preceding slide: "Can we estimate the 28-day compressive strength of a concrete mix without casting and crushing another cylinder?".

LECTURER CUE
A worked case from your own discipline: IF the crack is wider than 0.30 mm THEN flag it for repair — A code of practice gives you the threshold. You do not need data to write that rule. That belongs firmly in the left-hand column. The right-hand column earns its place when there is no threshold in any code of practice and no formula to look up, and you have examples of past cases instead. Neither column is better; the useful question is whether you already know the rule for the problem in front of you.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
When to write the rule, and when to learn it from data. Move on after a learner can explain the current example or required action.

## Slide 23 — When to write the rule, and when to learn it from data

TEACHING PURPOSE
When to write the rule, and when to learn it from data

CONNECT
Build on the preceding slide: Traditional programming, and machine learning.

LECTURER CUE
Most of engineering stays in the left-hand column and that is the correct place for it. The third item on the left is the one that decides real projects: a model whose decision cannot be explained line by line often cannot be used at all, whatever its accuracy on test data. That constraint returns in Week 12.

EXPLAIN IN ORDINARY WORDS
A value is a piece of information. A variable is a name referring to a value. In length_m = 5, Python evaluates the right side and binds that result to the name on the left.

CHECK AND EXPECTED ANSWER
After x=3 then x=5, what does print(x) display? 5. The earlier value is not added automatically.

IF LEARNERS ARE STUCK
Write the name on a card and the current value beside it. Distinguish number 3 from quoted text "3".

NEXT
What we actually mean by 'data'. Move on after a learner can explain the current example or required action.

## Slide 24 — What we actually mean by 'data'

TEACHING PURPOSE
What we actually mean by 'data'

CONNECT
Build on the preceding slide: When to write the rule, and when to learn it from data.

LECTURER CUE
This is the picture to fix in your head, because every dataset you meet this semester has this shape. One row is one example. The feature columns hold what you know beforehand and the target column holds the thing you want to predict. Worth thinking about: the target of one problem can be a feature of another. Curing temperature is the target if you are studying an oven and a feature if you are predicting strength.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Feature, and target. Move on after a learner can explain the current example or required action.

## Slide 25 — Feature, and target

TEACHING PURPOSE
Feature, and target

CONNECT
Build on the preceding slide: What we actually mean by 'data'.

LECTURER CUE
The 'association is not a cause' line is the seed of correlation versus causation, which arrives properly in Week 8. One error to start watching for now: including a column that is only known after the target is known. That is data leakage, it is the most destructive mistake in applied machine learning, and Week 10 is a full session on it.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 26 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Feature, and target.

LECTURER CUE
Write something for each of the three before you turn to the answers. Question B is deliberately hard for Week 1 — noticing that the repair column can only be filled in after the failure has happened is enough at this stage, even if you cannot yet name what is wrong with using it.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Feature or target?
The target. It is the thing you want to predict. Everything measured beforehand is a feature.
B
The repair column?
No. You only know what repair was done AFTER the failure, so it cannot help you predict the failure. Include it and your model will look brilliant in testing and be useless in service. This is called data leakage and we spend a whole session on it in Week 10.
C
A rule you already know?
Anything with a formula or a code threshold: For a simply supported beam under a uniform load, the bending moment has an exact formula. Use it. If a validated equation exists, use the equation.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 27 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

LECTURER CUE
Getting B wrong is normal; professional teams ship this bug regularly and only find it when the model reaches service. The name for it is data leakage. The timing test in answer B — could I know this column before the outcome? — is the one habit to carry out of this slide.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Hands on: predict case 13. Move on after a learner can explain the current example or required action.

## Slide 28 — Hands on: predict case 13

TEACHING PURPOSE
Hands on: predict case 13

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Teams of four or five, formed now and kept for the rest of the semester. You are about to do machine learning by hand, on paper, before anybody writes a line of code.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Your task. Move on after a learner can explain the current example or required action.

## Slide 29 — Your task

TEACHING PURPOSE
Your task

CONNECT
Build on the preceding slide: Hands on: predict case 13.

LECTURER CUE
The number your team predicts matters far less than the sentence saying how you got it, so write the reasoning down. The next three slides give names to whatever method you used, and that only works if you can still see what you did. If you are stuck, start with one question: which single column seems to move with the outcome, and why that one?

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Reading the pattern from twelve cases. Move on after a learner can explain the current example or required action.

## Slide 30 — Reading the pattern from twelve cases

TEACHING PURPOSE
Reading the pattern from twelve cases

CONNECT
Build on the preceding slide: Your task.

LECTURER CUE
There is no single right method, and this is one line of thinking that works. Step five is what separates an engineer from a calculator: how confident am I, and what would change my mind? The two practical tests, in Weeks 7 and 14, assess that step far more heavily than the arithmetic.

NEXT
The answer, and your error. Move on after a learner can explain the current example or required action.

## Slide 31 — The answer, and your error

TEACHING PURPOSE
The answer, and your error

CONNECT
Build on the preceding slide: Reading the pattern from twelve cases.

LECTURER CUE
The spread of team answers is the teaching point. Several different reasonable methods produced several different numbers, so being reasonable is not enough on its own — you need a way to measure which method is better. One case cannot tell you that, which is what Week 8 sets up.

NEXT
You just did every step of a machine learning project. Move on after a learner can explain the current example or required action.

## Slide 32 — You just did every step of a machine learning project

TEACHING PURPOSE
You just did every step of a machine learning project

CONNECT
Build on the preceding slide: The answer, and your error.

LECTURER CUE
The syllabus for the rest of the semester is largely a set of names for what you just did with a pencil. The fourth pair is the one to dwell on: you predicted a case that was not in front of you when you formed the rule. That is generalisation, and everything in Week 10 follows from it.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Break. Move on after a learner can explain the current example or required action.

## Slide 33 — Break

TEACHING PURPOSE
Break

CONNECT
Build on the preceding slide: You just did every step of a machine learning project.

LECTURER CUE
Ten minutes. The challenge segment after the break is the longest single working block of the session, so use the time.

NEXT
Two kinds of question. Move on after a learner can explain the current example or required action.

## Slide 34 — Two kinds of question

TEACHING PURPOSE
Two kinds of question

CONNECT
Build on the preceding slide: Break.

LECTURER CUE
A short segment carrying one distinction that decides which method you reach for all semester. It needs to be automatic by Week 8, when you start fitting models to both kinds of problem.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Regression and classification. Move on after a learner can explain the current example or required action.

## Slide 35 — Regression and classification

TEACHING PURPOSE
Regression and classification

CONNECT
Build on the preceding slide: Two kinds of question.

LECTURER CUE
The point that is easy to miss: the SAME dataset can pose either question. Take the target on the left and band it — strength class: below 25 MPa, 25 to 40, above 40 — and the regression problem has become a classification problem. Banding is an engineering decision with consequences, because it throws away the distance between two values inside the same band, and it comes back in Week 9 when you start choosing how to measure performance.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Regression, and classification. Move on after a learner can explain the current example or required action.

## Slide 36 — Regression, and classification

TEACHING PURPOSE
Regression, and classification

CONNECT
Build on the preceding slide: Regression and classification.

LECTURER CUE
Carry the test as a habit: what would the answer look like written down? A quantity with a unit means regression. A word or a label means classification. That question resolves almost every case you will meet, and it is faster than trying to remember the definitions.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Can you answer these?. Move on after a learner can explain the current example or required action.

## Slide 37 — Can you answer these?

TEACHING PURPOSE
Can you answer these?

CONNECT
Build on the preceding slide: Regression, and classification.

LECTURER CUE
Question C is the interesting one. It is still classification, with five categories rather than two. Multi-class problems are harder to evaluate because one accuracy figure hides which classes you are getting wrong, and that is a Week 9 topic.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Days until replacement?
Regression. The answer is a number with a unit — days.
B
Pass or fail?
Classification. Two categories, so it is called binary classification.
C
Which of five fault types?
Still classification, but multi-class rather than binary. It is harder: with five classes there are far more ways to be wrong, and a single accuracy figure hides which ones you get wrong. Week 9.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 38 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Can you answer these?.

LECTURER CUE
You now have vocabulary you can use immediately: binary classification for two categories, multi-class for three or more. The distinction starts to matter as soon as you begin measuring performance in Week 9, because the same accuracy figure means different things in the two cases.

EXPLAIN IN ORDINARY WORDS
Read each quantity and unit before using a formula. Python calculates numbers but does not enforce physical units. Parentheses specify which operation happens first.

CHECK AND EXPECTED ANSWER
What is 5 m times 3 m? 15 square metres. What is 7/2 in Python? 3.5; 7//2 is 3.

IF LEARNERS ARE STUCK
Write the formula and units on paper, substitute small values, then translate it to Python. Check zero denominators and the issued sign convention.

NEXT
What machine learning cannot do. Move on after a learner can explain the current example or required action.

## Slide 39 — What machine learning cannot do

TEACHING PURPOSE
What machine learning cannot do

CONNECT
Build on the preceding slide: How did you do?.

LECTURER CUE
Four honest limits, so that you can recognise in advance when data will not help. This is also your protection against being sold a technique that cannot work on the problem you have.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Four limits, and none of them go away. Move on after a learner can explain the current example or required action.

## Slide 40 — Four limits, and none of them go away

TEACHING PURPOSE
Four limits, and none of them go away

CONNECT
Build on the preceding slide: What machine learning cannot do.

LECTURER CUE
The caption is the sentence to remember. A machine learning method will always return an answer and will never tell you that the question was unanswerable. Judging that is your job, and it is the reason a trained engineer is still needed after the code runs.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
The same four limits, in your own discipline. Move on after a learner can explain the current example or required action.

## Slide 41 — The same four limits, in your own discipline

TEACHING PURPOSE
The same four limits, in your own discipline

CONNECT
Build on the preceding slide: Four limits, and none of them go away.

LECTURER CUE
Every project in Week 9 has to survive these four questions before it is approved. A team that cannot answer them has picked a technique and gone looking for somewhere to use it, which is the most common way a student project fails.

EXPLAIN IN ORDINARY WORDS
A function is a named set of instructions. def defines it; a call runs it with inputs. Parameters are input names, arguments are supplied values, and return sends the result back.

CHECK AND EXPECTED ANSWER
Does print(8) return the number 8 to the caller? No; it displays 8 and returns None. A function needing a numeric result should return it.

IF LEARNERS ARE STUCK
Trace one call: bind input names, run the indented body, reach return, then put the returned result back into the calling expression.

NEXT
Challenge: the Problem Hunt. Move on after a learner can explain the current example or required action.

## Slide 42 — Challenge: the Problem Hunt

TEACHING PURPOSE
Challenge: the Problem Hunt

CONNECT
Build on the preceding slide: The same four limits, in your own discipline.

LECTURER CUE
In this segment you get a problem and no method, and the questions you are asked will not be answered for you. Proceeding without instructions is the skill being practised, and roughly one segment of every session this semester works this way.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Problem Hunt. Move on after a learner can explain the current example or required action.

## Slide 43 — Problem Hunt

TEACHING PURPOSE
Problem Hunt

CONNECT
Build on the preceding slide: Challenge: the Problem Hunt.

LECTURER CUE
The rejections carry more weight than the acceptances. A team that can say clearly why something is NOT a machine learning problem has understood the session, and the six questions on the slide are the ones to argue each placement against. Keep your sheet: the class list of problems built in this segment is what teams draw on when they choose projects in Week 9.

EXPLAIN IN ORDINARY WORDS
A list keeps items in order. Python positions start at zero. In [2,4,6], position 0 contains 2 and position 2 contains 6. A slice excludes its stop position.

CHECK AND EXPECTED ANSWER
What is [2,4,6][1]? 4. Is there a position 3? No.

IF LEARNERS ARE STUCK
Draw three numbered boxes starting at zero. Keep the position separate from the value stored in it.

NEXT
How your team works, all semester. Move on after a learner can explain the current example or required action.

## Slide 44 — How your team works, all semester

TEACHING PURPOSE
How your team works, all semester

CONNECT
Build on the preceding slide: Problem Hunt.

LECTURER CUE
Sign the team charter before you leave: names, contact details, a weekly meeting slot, and what you will do if somebody stops contributing. Agreeing that in Week 1 is far easier than agreeing it in November, and the charter is the document your contribution log gets read against.

EXPLAIN IN ORDINARY WORDS
A repository is the project folder and recorded history. A commit records a chosen change; uploading or pushing shares it. A README tells someone else how to run the work.

CHECK AND EXPECTED ANSWER
Does saving to GitHub hand in the assignment? No; submission requires the correct form and its confirmation.

IF LEARNERS ARE STUCK
Ask a partner to follow only the README. It should identify the data, files, run order and expected result. Keep secrets out of the repository.

NEXT
Gallery walk, and what you owe me. Move on after a learner can explain the current example or required action.

## Slide 45 — Gallery walk, and what you owe me

TEACHING PURPOSE
Gallery walk, and what you owe me

CONNECT
Build on the preceding slide: How your team works, all semester.

LECTURER CUE
Gallery walk: your team visits two other teams' boards and writes one question on each sheet. Questions only, no verdicts. This is the first peer review of the semester, and in Week 13 peer review is graded.

NEXT
Before Week 2. Move on after a learner can explain the current example or required action.

## Slide 46 — Before Week 2

TEACHING PURPOSE
Before Week 2

CONNECT
Build on the preceding slide: Gallery walk, and what you owe me.

LECTURER CUE
The 'not solvable' item is the most valuable part of A1, because it forces you to use the four limits rather than remember them. Take the instruction not to install anything seriously: the course runs in Google Colab, and a Python installation you set up at home creates a problem that cannot be diagnosed in class.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

ASSIGNMENT HANDOVER
Open the matching public student guide and show the exact starter filename, required outputs and upload set. Ask one learner to repeat what to submit and where. IUEA Student Registration Number is required freeform text; learners enter their own number. A saved repository is not a submitted form. Read the live deadline and keep the submission confirmation. Do not release an assessment that is still awaiting grading validation.

A1 CATCH-UP
The original Week 1 schedule has been superseded for catch-up collection. Use the current cohort A1 form deadline, aligned with its Week 2 assignment upload. Quiz 1 is separate and gets 24 hours from its own activation.

NEXT
Watch this before Week 2. Move on after a learner can explain the current example or required action.

## Slide 47 — Watch this before Week 2

TEACHING PURPOSE
Watch this before Week 2

CONNECT
Build on the preceding slide: Before Week 2.

LECTURER CUE
Watch for where he draws the boundaries between the four terms, and whether they match the nested diagram from today. If they differ, raise it next week — the field genuinely does not fully agree on this. Two optional extras: StatQuest, 'A Gentle Introduction to Machine Learning', https://www.youtube.com/watch?v=Gv9_4yMHFhI, whose author Josh Starmer is the spine of Weeks 8 to 12; and if you have ninety seconds only, Fireship, 'Machine Learning Explained in 100 Seconds', https://www.youtube.com/watch?v=PeMlggyqz0Y

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

VIDEO ROUTINE
Preview the exact link and stated excerpt before class. State the viewing question first, pause after the example, and ask a learner to explain it. If access fails, use the adjacent worked example and discussion rather than spend class time troubleshooting streaming.

NEXT
Revision material. Move on after a learner can explain the current example or required action.

## Slide 48 — Revision material

TEACHING PURPOSE
Revision material

CONNECT
Build on the preceding slide: Watch this before Week 2.

LECTURER CUE
Everything from here on is revision material rather than presented content: a summary, a self-test with worked answers, an eighteen-term glossary and a one-page reference sheet. It is written to be studied from in your own time.

NEXT
What you should take away. Move on after a learner can explain the current example or required action.

## Slide 49 — What you should take away

TEACHING PURPOSE
What you should take away

CONNECT
Build on the preceding slide: Revision material.

LECTURER CUE
Seven statements covering the whole session. If any of them reads as new to you, go back to the slide it came from before Week 2 rather than after it.

EXPLAIN IN ORDINARY WORDS
Missing means not recorded, not automatically zero. Decide why it is missing and document the rule. Fitted fill values must come from training data when evaluating a model.

CHECK AND EXPECTED ANSWER
Is an unrecorded energy reading evidence of zero consumption? No.

IF LEARNERS ARE STUCK
Use three rows: a recorded zero, a recorded positive value and a blank. Explain their different meanings before cleaning.

NEXT
Self-test — try these before you look. Move on after a learner can explain the current example or required action.

## Slide 50 — Self-test — try these before you look

TEACHING PURPOSE
Self-test — try these before you look

CONNECT
Build on the preceding slide: What you should take away.

LECTURER CUE
Optional revision, best attempted with a pencil before you look at the next slide. Question D is a Week 10 idea planted early: anything that notices the circularity of testing a model on cases it has already seen is a good answer at this stage.

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

DISCUSSION KEY FOR THIS SLIDE
ANSWERS
How did you do?
A
Three questions before agreeing to 'use AI'?
What exactly are we predicting? What data exists, who measured it, and is it kept? And would a rule or an equation we already have do this better? If any of those has no answer, stop.
B
Features and target in a repair table?
The target is whatever you want to predict — say time to next failure. Features are everything known BEFORE that: operating hours, load, temperature. The test is timing: anything only known afterwards cannot be a feature.
C
One of each from your discipline?
Regression: any quantity with a unit — 28-day compressive strength in MPa. Classification: strength class: below 25 MPa, 25 to 40, above 40.
D
Why is a good fit on seen data not evidence?
Because the model could simply have memorised those cases. The only honest test is performance on examples it has never seen — exactly what you did with case 13. This is the whole subject of Week 10.
E
What else before acting?
How large the error is in engineering terms and whether that is tolerable; what it costs when the model is wrong; and whether today's conditions still resemble the data it learned from.
Let learners attempt first; use this to explain the reasoning, not just reveal the answer.

NEXT
How did you do?. Move on after a learner can explain the current example or required action.

## Slide 51 — How did you do?

TEACHING PURPOSE
How did you do?

CONNECT
Build on the preceding slide: Self-test — try these before you look.

LECTURER CUE
Answer D is the most important idea in the course. A model can simply memorise the cases it was shown, so good performance on those cases is no evidence of anything. The only honest test is data the model has never seen, which is exactly what case 13 was for you.

EXPLAIN IN ORDINARY WORDS
A condition is a True/False question. Python executes the matching indented branch. = assigns; == compares. >= includes the boundary, while > excludes it.

CHECK AND EXPECTED ANSWER
With value 30, is value >= 30 true? Yes. Is value > 30 true? No.

IF LEARNERS ARE STUCK
Try one value below, at and above the boundary before running the code.

NEXT
Every word we used today (1 of 3). Move on after a learner can explain the current example or required action.

## Slide 52 — Every word we used today (1 of 3)

TEACHING PURPOSE
Every word we used today (1 of 3)

CONNECT
Build on the preceding slide: How did you do?.

EXPLAIN IN ORDINARY WORDS
A cleaning decision needs evidence, a stated rule and a before/after check. Similar rows may be genuine repeated events. Reconciliation compares totals built under the same definitions.

CHECK AND EXPECTED ANSWER
May we delete every repeated amount? No. Check the row identifier and the table grain first.

IF LEARNERS ARE STUCK
Keep raw data, record counts before and after each action, then explain any remaining difference instead of forcing totals to agree.

NEXT
Every word we used today (2 of 3). Move on after a learner can explain the current example or required action.

## Slide 53 — Every word we used today (2 of 3)

TEACHING PURPOSE
Every word we used today (2 of 3)

CONNECT
Build on the preceding slide: Every word we used today (1 of 3).

EXPLAIN IN ORDINARY WORDS
A feature is an input available when predicting. The target is the answer to learn from. Regression predicts a number; classification predicts a category. Learning patterns does not by itself establish cause.

CHECK AND EXPECTED ANSWER
Predicting concrete strength: regression. Predicting pass/fail: classification. Is a later test result available before that test? No.

IF LEARNERS ARE STUCK
Describe the engineering decision in everyday language, then label one row, an input and its answer. Compare with a rule you could write directly.

NEXT
Every word we used today (3 of 3). Move on after a learner can explain the current example or required action.

## Slide 54 — Every word we used today (3 of 3)

TEACHING PURPOSE
Every word we used today (3 of 3)

CONNECT
Build on the preceding slide: Every word we used today (2 of 3).

LECTURER CUE
Eighteen terms. If you can define all eighteen by Week 3 you are ahead of the schedule, and these exact words appear in the weekly quizzes. The last two entries, generalisation and association versus cause, are forward references; they are printed here so the words are familiar when they arrive properly in Weeks 8 and 10.

EXPLAIN IN ORDINARY WORDS
Training fits rules. Validation helps choose among rules. The final test estimates performance after choices are fixed. Information that would be unavailable at the real prediction time must stay out of the inputs.

CHECK AND EXPECTED ANSWER
May two readings of the same machine appear on both sides when evaluating new machines? No; split by machine. For forecasting, train on the past and evaluate later time.

IF LEARNERS ARE STUCK
Use three envelopes. Keep the final-test envelope closed while selecting features or settings.

NEXT
Eight questions to ask about any data problem. Move on after a learner can explain the current example or required action.

## Slide 55 — Eight questions to ask about any data problem

TEACHING PURPOSE
Eight questions to ask about any data problem

CONNECT
Build on the preceding slide: Every word we used today (3 of 3).

LECTURER CUE
These eight questions are the spine of the whole course. Every project milestone from Week 9 onwards is assessed against some subset of them, and this is the page worth having in front of you in the Week 14 practical test.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

NEXT
Five questions,. Move on after a learner can explain the current example or required action.

## Slide 56 — Five questions,

TEACHING PURPOSE
Five questions,

CONNECT
Build on the preceding slide: Eight questions to ask about any data problem.

LECTURER CUE
The last five minutes of every teaching session. Five questions, one per cent, and you see your score as you submit.
Nothing on it can be answered without reading what it shows you, so there is nothing to revise for it beyond having done the session. Twelve run across the semester and the best ten count.

EXPLAIN IN ORDINARY WORDS
An observation describes the data. A finding answers a defined question with evidence. A recommendation adds an action, its justification and limits.

CHECK AND EXPECTED ANSWER
Does a difference between two groups prove one caused the other? No. Other differences or selection may explain it.

IF LEARNERS ARE STUCK
Ask for the population, time period, number and comparison. Then ask what additional evidence could change the recommendation.

QUIZ OPERATION
Opening the student link does not activate the quiz. In Quiz Controls run the matching open_W<week>_<cohort> function once when ready. Announce the logged closing time: 24 hours after activation. Five minutes describes expected answering time, not the availability window. Quiz 1 and Quiz 2 require separate activation when collecting catch-up work.

NEXT
You have already done. Move on after a learner can explain the current example or required action.

## Slide 57 — You have already done

TEACHING PURPOSE
You have already done

CONNECT
Build on the preceding slide: Five questions,.

LECTURER CUE
Before next week: A1 due at the start of the session, a GitHub account and a Google account created, the video watched, and nothing installed. Week 2 needs a browser and nothing else.

EXPLAIN IN ORDINARY WORDS
A notebook contains code cells and explanatory text cells. The runtime remembers values from cells that actually ran, which may differ from their visual order.

CHECK AND EXPECTED ANSWER
Does editing a cell update a value already stored in memory? No; the cell must run.

IF LEARNERS ARE STUCK
Outside an assessment restriction, restart and run from the top after loading data. Fix the first error before later cells; save the successful notebook.

