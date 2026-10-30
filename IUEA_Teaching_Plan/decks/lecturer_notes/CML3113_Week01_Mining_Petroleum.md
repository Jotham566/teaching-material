# CML3113 Week 1

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: AI, machine learning
and the engineering problem

Introduction to Machine Learning in Mining & Petroleum Engineering

WEEK 1  ·  Fri 11 September 2026

Friday 08:00–11:00 · Room 105  ·  IUEA Faculty of Engineering · Semester 1, 2026/27

**Spoken script**

Welcome to week one of Machine Learning. Today's session is called AI, machine learning and the engineering problem. This course introduces machine learning through examples from mining and petroleum engineering, such as ore processing and reservoirs. We start from zero. You do not need any programming experience for today, and we will explain every new word as we meet it. Check the slide for your day, time and room.

## Slide 2: Jotham Martin Wambi

Data scientist and ML engineer · Founding engineer, Magentiq AI Labs

Background

Some of what I have built

Incoming PhD student (April 2027)
Osaka Metropolitan University, Japan

Master of Technology Management
Yamaguchi University, Japan

BSc IT, Makerere · BA Economics, IUIU

Eight years at Citibank, EY and D'isum Inc, Tokyo

Law Lens

Language models over Ugandan law, fully traceable.

Magentiq AssetGuard

Machine failure predicted from vibration sensors.

Wearable ECG detection

Eleven cardiac conditions from a live ECG.

Every system on the right uses the pipeline you build from Week 8: split the data, fit a model, then score it.

linkedin.com/in/jothammartinwambi   ·   github.com/Jotham566   ·   jothammartin.wambi@gmail.com

**Spoken script**

I am Jotham Martin Wambi, and I will be your lecturer for this course. By training I am a data scientist and machine learning engineer, and I am a founding engineer at Magentiq AI Labs.

My background is in information technology and economics, with a master's degree in technology management from Yamaguchi University in Japan. I will start a PhD at Osaka Metropolitan University in April next year. Before that I worked for eight years at Citibank, at EY and at D'isum Inc in Tokyo.

Here are three systems I have helped build. Law Lens is a system that answers questions about Ugandan law and shows where each answer came from. AssetGuard predicts when a machine will fail, using vibration sensors. The third reads a live heart signal from a wearable device and recognises eleven heart conditions.

All three follow the same pipeline that you will build from Week 8. We split the data, fit a model, and then score it. My contact details are on the slide.

## Slide 3: By the end of today you can…

1

Say what artificial intelligence, machine learning and data science each mean, and how they differ.

2

Explain the difference between writing a rule yourself and letting a computer infer one from examples.

3

Point at a table of data and correctly identify the features and the target.

4

Tell a regression problem from a classification problem, and give an example of each from your own field.

5

Name three problems in exploration, ore and reservoir characterisation, production and equipment health where data could help, and two where it could not.

6

State four things machine learning cannot do, with a reason for each.

7

Describe how this course is assessed and what your project will look like.

Week 1 · AI, machine learning and the engineering problem · nothing here needs prior programming experience

**Spoken script**

These are the seven things you should be able to do by the end of today. Read them as questions that you will be able to answer.

We begin with words. You will be able to say what artificial intelligence, machine learning and data science each mean, and how they differ. Then you will explain the difference between writing a rule yourself and letting a computer work out a rule from examples.

Next comes the data. You will look at a table and say which columns are the features, which are the inputs, and which column is the target, the thing we want to predict. You will also tell a regression problem, where the answer is a number, from a classification problem, where the answer is a category.

Objective five asks you to name three problems in exploration, ore and reservoir characterisation, production and equipment health where data could help, and two where it could not. Objective six is to state four things machine learning cannot do, with a reason for each. Objective seven is to describe how the course is assessed and what your project will look like. Nothing today needs programming experience.

## Slide 4: How every session this semester is shaped

Three hours, eleven segments. No block of talking runs longer than 25 minutes, and roughly half of every session is you doing something rather than me saying something.

**Spoken script**

Every session this semester has the same shape, so you always know what is coming. Each session lasts three hours and is split into eleven segments.

No stretch of talking from me runs longer than twenty five minutes. After each short explanation you do something yourself, such as answering a question, working through a small example or solving a problem on paper. Roughly half of every session is you doing and half is me explaining.

Today's segments follow the same pattern. We define the main ideas, we work through an example together, and then you try one on your own. Use the segment slides to see where we are and how long each part should take.

## Slide 5: Where this semester goes

Fifteen weeks. Weeks 7 and 14 are practical tests: you are given data you have never seen and asked what you make of it. The project runs from Week 9 to the last session.

**Spoken script**

This slide shows the whole semester. It has fifteen weeks.

The early weeks set you up and teach the basics of Python, which is the programming language we use, and how to prepare data. Weeks 7 and 14 are practical tests. In a practical test you are given a data set you have never seen before, and you are asked what you make of it. This tests whether you can work with real data. You prepare for it by doing the weekly exercises.

The project runs from Week 9 to the last session. You will work on it in a team, and I will explain how teams work later today.

Keep this slide in mind when you plan your own time. Check the slide for the weeks that matter most.

## Slide 6: What you will be able to say by December

The course builds from reading data to testing a model. Weekly exercises give you practice at each stage.

**Spoken script**

By December you should be able to say several things with confidence, and this slide lists them. The course builds in order. First you learn to read data. Then you clean it and summarise it. Finally you build a model and test whether it works.

Each week has an exercise that practises one stage of that route. You show what you can do. That means a notebook that runs, a summary that is correct, a chart whose reasoning you can explain, or a model whose results you have checked.

In every calculation we also keep the engineering meaning, including the units. A number without a unit tells an engineer very little.

## Slide 7: Welcome, and how this course works

Course goals, assessment and weekly work.

**Spoken script**

This is the first segment, and it lasts fifteen minutes. In it we cover three things. These are the goals of the course, how it is assessed, and the work you do each week.

The course has two kinds of work. Some is individual, and some is done with a team in a project. We keep these separate so that you always know what you are submitting and who it is for. The next slide gives the assessment components and what each one is worth.

A weekly task is a small piece of work. A project milestone is a stage of your team project. They are different, and you do not hand in one in place of the other.

## Slide 8: How you are assessed

Assessment includes code, data analysis, models and written explanations. Individual work accounts for 65% of the mark.

**Spoken script**

Here is how your marks are built. Assessment includes code, data analysis, models and written explanations. So you will write short pieces of code, analyse data, build models, and explain in writing what you did and what you found.

Individual work accounts for sixty five per cent of the mark. That means most of your result depends on what you can do yourself.

The slide lists the components and their weights, and together they add up to one hundred per cent. Some weekly tasks and quizzes can differ by cohort, so check the details for your own class on the course page. Read the marking criteria for each piece of work before you start it.

## Slide 9: What I expect, and what you can expect back

What I expect from you

Attend. There is one three-hour session a week and no lecture to catch up from — the value is in the practical and the challenge, which cannot be read later.

Do the weekly deliverable every week. Eleven small pieces spread over twelve weeks is manageable; nine of them attempted in December is not.

When asking for help, include the error message, what you tried and what you expected.

When you get stuck, note the step that failed and ask for help.

What you can expect from me

Every rubric published before the work is set. You will never meet a marking scheme for the first time in an assessment.

Download the lesson files before class so you can access the data without a connection.

Feedback on the weekly work within a week, and instant feedback on every quiz.

Ask how each topic relates to the engineering problem.

**Spoken script**

This slide sets out what I expect from you, and what you can expect from me.

First, attend. There is one three hour session a week. The value is in the practical work and the challenge, and you cannot read that later. Second, do the weekly deliverable every week. Eleven small pieces spread over twelve weeks is manageable. Trying nine of them in December is not.

When you ask for help, include the error message, what you tried and what you expected to happen. When you get stuck, note the step that failed and ask.

From me, you get every marking scheme before the work is set, so you never meet a rubric for the first time in an assessment. You get feedback on weekly work within a week, and instant feedback on every quiz. I also ask you to download the lesson files before class so that you can use the data without an internet connection. And ask how each topic relates to your engineering problem.

## Slide 10: Machine learning topics

This roadmap shows Semester 1, Semester 2 and topics outside this course.

**Spoken script**

This is the second segment, and it lasts fifteen minutes. It is about the topics of machine learning, so it is a map of the whole field.

A roadmap puts ideas and tools in order. It shows what comes first, what builds on what, and where you are going. The next slide shows a roadmap with fifteen stages. Some of those stages we cover in Semester 1, some belong to Semester 2, and some this course does not teach at all.

You do not need to learn every item today. Your job in this segment is to see the whole landscape once, so that each later week has a place on the map.

## Slide 11: The machine learning roadmap

Fifteen stages, from Python to transformers. Orange is Semester 1. Green is Semester 2. Dark blue is the stage you already have from your engineering degree. Grey is what this course deliberately does not teach. Structure follows the public roadmap.sh Machine Learning roadmap.

**Spoken script**

This is the roadmap for machine learning. It has fifteen stages, running from Python at the start to transformers at the end. A transformer is the type of model behind modern chatbots, and we only meet it much later.

The colours carry the meaning. Orange stages are taught in Semester 1. Green stages are taught in Semester 2. Dark blue is the stage you already have from your engineering degree. Grey marks what this course deliberately does not teach.

The shape follows the public roadmap dot sh Machine Learning roadmap, which is a free guide that many learners use.

The orange stages are your route this semester. You start with Python, move to preparing data, and then reach building and testing models.

## Slide 12: Mathematics and programming foundations

Mathematics used in machine learning

The roadmap includes calculus, linear algebra, statistics and probability. Each supports a different part of building or evaluating a model.

We introduce the mathematics needed for each topic, including averages, matrices and probability. Earlier mathematics courses may help, but each example includes the steps.

Programming foundations

Weeks 2–6 introduce Python, data libraries and data preparation through worked examples.

Applying engineering knowledge

This course introduces programming through engineering examples.

Engineering knowledge helps you check units, judge whether a result is plausible and recognise limits in the data.

**Spoken script**

Machine learning rests on two foundations, mathematics and programming. We will meet both, and we will not assume that you have mastered either.

The roadmap lists calculus, which is the mathematics of change, linear algebra, which is working with lists and tables of numbers, statistics, which is summarising data, and probability, which measures how likely something is. Each one supports a different part of building or checking a model.

We introduce only the mathematics that each topic needs, such as averages, matrices and probability, and each example shows the steps. Earlier mathematics courses may help, but you can follow without them.

For programming, Weeks 2 to 6 introduce Python, data libraries and data preparation through worked examples. A library is a ready made collection of code that we borrow.

Your engineering knowledge matters too. It helps you check units, judge whether a result is plausible, and see the limits of the data.

## Slide 13: Topics covered in this course

Grey marks topics outside this course, including reinforcement learning, full MLOps and most advanced language-model topics.

**Spoken script**

The grey boxes on the roadmap are topics outside this course. They include reinforcement learning, full MLOps and most advanced language model topics.

Reinforcement learning is a way for a program to learn by trying actions and receiving rewards. MLOps is the work of running a model in production, which means watching it and updating it after it has been deployed. Language models are the systems that work with text. We touch the idea, but we do not go deep.

Read this boundary literally. If a topic sits outside the highlighted route, it is not a hidden prerequisite for any weekly task. Nobody will ask you to use it in an exercise or a test. Those topics exist, and you can study them later if you wish.

## Slide 14: Four jobs this field splits into

These are four different roadmaps and four different careers. This course points at the first one, applied inside your own engineering discipline — which is a narrower and more defensible position than competing with computer science graduates on general machine learning.

**Spoken script**

Work with data splits into four different jobs. The slide calls them four different roadmaps and four different careers.

A data analyst explains what the data shows. A data scientist investigates a question using data. A machine learning engineer builds and runs prediction systems. A data engineer makes sure that reliable data arrives where it is needed.

Our course aims at the job of applying data skills inside your own engineering field. That is a narrower position, and it is a strong one. You bring engineering knowledge that computer science graduates do not have.

The course gives you introductory skills in this area. It is a start and it does not replace a professional qualification.

## Slide 15: Machine learning in engineering

Three words people use interchangeably and should not — and where engineering sits among them.

**Spoken script**

This is the third segment, and it takes fifteen minutes. Three words are used as if they meant the same thing, and they do not. They are artificial intelligence, machine learning and data science.

In this segment we separate them, and we place engineering among them. Each gets its own slide with a definition, an example and a common confusion.

When we choose a method, we start from the decision that someone needs to make, and from the observations we already have. We choose a model after that. If you pick a model first, you can reach an impressive score that helps nobody.

## Slide 16: The words, and how they nest

Each is contained by the one before it. Data science is the odd one out: it overlaps all of them and is contained by none, because it is the craft of getting an answer out of data at all — finding it, cleaning it, questioning it, presenting it.

**Spoken script**

Three of these ideas nest inside one another: artificial intelligence, then machine learning, then deep learning. Data science sits outside that nesting. Artificial intelligence is the biggest circle. Machine learning is an approach inside artificial intelligence. Deep learning is a family of machine learning methods, and it uses large networks of simple calculations called neural networks. So each one is contained by the one before it.

Data science is the odd one out. It overlaps all of them and is contained by none of them. Data science is the craft of getting an answer out of data at all. That includes finding the data, cleaning it, questioning it and presenting it.

Much of that work involves no model whatever. A person who counts missing readings, checks units, and explains a trend is doing data science, even if no predictive model is ever built.

## Slide 17: Artificial intelligence

Any machine doing something we would call intelligent. It names a goal. Many different techniques aim at it.

A chess engine is AI. So is a spam filter. A thermostat is not — it follows one fixed rule with no notion of doing better.

Machine learning, which is one particular way of achieving AI. All machine learning is AI; most AI historically was not machine learning.

**Spoken script**

Artificial intelligence means any machine doing something that we would call intelligent. It names a goal. Many different techniques aim at that goal.

For example, a chess engine is artificial intelligence. So is a spam filter, which sorts unwanted email. A thermostat is not, because it follows one fixed rule and has no notion of doing better.

This is easy to confuse with machine learning. Machine learning is one particular way of achieving artificial intelligence. All machine learning is artificial intelligence. Most artificial intelligence in history was never machine learning, because it ran on rules that people wrote by hand.

So the phrase artificial intelligence tells you what someone wants to achieve. It does not tell you how they do it, and it does not mean that the system understands the problem the way a person does.

## Slide 18: Machine learning

Getting a computer to work out a rule from examples, instead of you writing the rule yourself.

You show it six months of process readings every twenty seconds, each with the assay that came back later. It infers a relationship. You then decide whether to trust it.

Automation. A script that emails a report every Monday is automation and there is no learning in it at all.

**Spoken script**

Machine learning means getting a computer to work out a rule from examples..

Here is an example. You show the computer six months of process readings, taken every twenty seconds. Each reading is matched with the assay result, the laboratory measurement, that came back later. The computer looks through all of these examples and infers a relationship between the readings and the outcome. After that, you decide whether to trust it. The computer does not decide that for you.

Do not confuse machine learning with automation. A script that emails a report every Monday is automation. It does exactly what it was told, and there is no learning in it at all.

## Slide 19: Data science

The craft of getting a trustworthy answer out of data — finding it, cleaning it, questioning it, analysing it and presenting it so somebody can act.

Discovering that a third of your assay records are missing, working out whether they are missing at random, and deciding what that does to your conclusion. No model involved.

Machine learning. You will spend far more of this semester on data science than on machine learning, and that ratio matches professional practice.

**Spoken script**

Data science is the craft of getting a trustworthy answer out of data. The steps are finding the data, cleaning it, questioning it, analysing it, and presenting it so that somebody can act.

For example, you might discover that a third of your assay records are missing. You then work out whether they are missing at random, or whether there is a reason, and you decide what that does to your conclusion. No model is involved in any of this work.

Do not confuse data science with machine learning. You will spend far more of this semester on data science than on machine learning. That ratio matches professional practice, where most of the effort goes into getting the data right.

## Slide 20: Two ways to make a computer decide

Learning patterns from data and using them to make predictions.

**Spoken script**

This is the fourth segment, and it takes twenty five minutes. It is about two ways to make a computer decide something. Both ways take some inputs and produce an output. What differs is how the connection between the two is found.

In the first way, a person writes the rule. In the second way, the computer learns the rule from examples of inputs and the answers that went with them. Learning patterns from data and using them to make predictions is the second way.

Neither way is always better. If an established equation exists and its assumptions apply, the equation can be the better choice. We will work out together when each way fits.

## Slide 21: "The silica assay takes an hour to come back from the laboratory. Can we know it now, from the process variables we already measure?"

Hold onto that question. In twenty minutes you are going to answer a version of it yourself, on paper, with no computer and no formula.

**Spoken script**

Here is the question this course starts from. The silica assay takes an hour to come back from the laboratory. Can we know it now, from the process variables we already measure?

An assay is a laboratory test that measures how much of a substance a sample contains. Silica is an impurity in the concentrate. Waiting an hour means the plant keeps running without knowing the answer.

Keep that question in mind. Think about what you would need. You would need past assay results, and the process measurements taken at the same times. In twenty minutes you will answer a version of it yourself, on paper, with no computer and no formula.

## Slide 22: Traditional programming, and machine learning

On the left, a rule specified by a person: you work out the rule and write it down. On the right, the new way: you do not know the rule, but you have examples of inputs and the answers that followed, and the computer works out a rule from them.

**Spoken script**

This slide shows the actual idea of the course. It compares two ways of working.

The first is traditional programming. You work out the rule yourself and write it down. The computer takes your rule and some inputs, and it produces answers. If you know that power equals voltage times current, you can write that rule yourself.

The second is machine learning. Here you do not know the rule. What you have are examples. Each example has the inputs and the answer that followed. You give both to the computer, and the computer works out a rule from them.

After that, the rule it found can be used on new inputs, and it predicts the answers. So the roles are reversed. In traditional programming you supply the rule. In machine learning the computer supplies the rule, and you supply the examples.

## Slide 23: When to write the rule, and when to learn it from data

Write the rule yourself when…

A code of practice, a datasheet or a validated equation already gives you the answer.

The relationship is simple and well understood.

You must be able to explain the decision to a client or a regulator line by line.

You have little or no historical data.

Let the computer infer the rule when…

Nobody knows the rule, or it involves many variables interacting.

You have a reasonable quantity of past examples where you know both the inputs and the outcome.

An early estimate can help with planning if its error is small enough for the decision.

You can test the inferred rule against cases it has never seen.

**Spoken script**

How do you choose between the two ways? This slide gives you the criteria.

Write the rule yourself when a code of practice, a datasheet or a validated equation already gives you the answer. Write it yourself when the relationship is simple and well understood. Write it yourself when you must explain every decision, line by line, to a client or a regulator. And write it yourself when you have little or no historical data.

Let the computer infer the rule when nobody knows the rule, or it involves many variables acting on each other. Choose this when you have a reasonable number of past examples where you know both the inputs and the outcome. An early estimate can help with planning, if its error is small enough for the decision. Finally, you must be able to test the inferred rule on cases it has never seen.

An equation still needs correct units and valid assumptions, so the check is always yours.

## Slide 24: Data, features and targets

In this example, each row describes one case. Feature columns contain the inputs available before prediction. The target column contains the value to predict.

**Spoken script**

Now we meet the vocabulary for data. Look at the table on the slide. Each row describes one case, which means one thing that was observed, such as one machine at one moment.

The columns are the measurements. Some columns are the inputs. We call these the feature columns. They hold the information that we have available before we make a prediction. One column holds the value that we want to predict. We call that the target column.

When you read any table, begin with the column names and the units. Then ask which columns you would really know in advance, and which one column is the answer. The table on the slide is part of the lesson, so there is no file to download or open.

## Slide 25: Feature, and target

A FEATURE is a column you know before the outcome — an input. The TARGET is the column you want to predict. One row containing all of them is one EXAMPLE.

In the table you just saw, iron feed grade, starch flow and pulp pH are the features. Silica in the concentrate is the target.

A target is not the same as a cause. Starch flow is associated with concentrate quality; the model learns the association and knows nothing about surface chemistry.

**Spoken script**

A feature is a column whose value you know before the outcome. It is an input. The target is the column you want to predict. One row that holds all of them is called one example.

In the table you just saw, iron feed grade, starch flow and pulp pH are the features. Silica in the concentrate is the target. The concentrate is the valuable material collected at the end of the process.

Be careful about the word cause. A target does not have to be a cause. Starch flow is associated with concentrate quality, which means the two tend to move together. The model learns that association. It knows nothing about surface chemistry, which is how the chemicals act on the mineral surfaces.

## Slide 26: Can you answer these?

In a table of froth flotation process data records, is silica in the concentrate a feature or the target?

You want to predict how long a pump will run before it fails. You have a column recording the repair that was carried out afterwards. Should it be a feature? Why or why not?

Give one example from your own discipline of a problem where you already know the rule, so machine learning would be the wrong tool.

Answers are on the next slide — try first, then look.

**Spoken script**

Here are three questions to try before we look at the answers. Take a minute to think about each one and write something down.

Question A. Take a table of froth flotation process data. Is the silica in the concentrate a feature or the target?

Question B. You want to predict how long a pump will run before it fails. You have a column that records the repair carried out afterwards. Should that column be a feature? Say why or why not. Think about when each piece of information becomes known.

Question C. Give one example from your own discipline of a problem where you already know the rule, so machine learning would be the wrong tool.

The answers are on the next slide. Try first, then look.

## Slide 27: How did you do?

Feature or target?

The target. It is the thing you want to predict. Measurements available beforehand are candidate features.

The repair column?

No. The repair is recorded after the failure, so it is unavailable at prediction time. Including it would give misleading test results. This is data leakage.

A rule you already know?

Anything with a formula or a code threshold: Contained metal is tonnage times grade. That is arithmetic; there is nothing to predict. If a validated equation exists, use the equation.

**Spoken script**

Let us check your answers.

For A, the answer is the target. The target is the thing you want to predict. The measurements that you have available beforehand are the candidate features.

For B, the repair column should not be a feature. The repair is recorded after the failure, so it is unavailable at the moment you need to predict. If you include it, your test results will look better than they should. This mistake has a name, data leakage. It means that information from the future has slipped into the inputs.

For C, any problem with a formula or a code threshold works. Contained metal is tonnage times grade. That is simple arithmetic, and there is nothing to predict.

If a validated equation exists, use the equation.

## Slide 28: Hands on: predict case 13

Use the twelve rows of data to predict a value for the new case. Write your prediction and explain which rows helped you choose it.

**Spoken script**

This is the fifth segment. It is hands on work and it takes twenty five minutes.

You get a table with twelve rows. Each row is a case with its inputs and its measured outcome. A thirteenth case is also given, and for that case only the inputs are shown. Your job is to predict its outcome.

Write down your prediction and explain which of the twelve rows helped you choose it. This is a paper exercise. You do not write code, and you do not train anything.

The aim is a reasoned estimate. The aim is a reasoned estimate, and what we mark is the reason you give.

## Slide 29: Your task

Twelve cases show their inputs and measured outcomes. Case 13 shows only its inputs. Predict its outcome and write one sentence explaining your choice.

**Spoken script**

Here is your task, and you have fifteen minutes for it. You work on your own.

Twelve cases show their inputs and their measured outcomes. Case thirteen shows only its inputs. Predict the outcome of case thirteen, and write one sentence explaining your choice.

Start by reading the column headings and the units. Then find the known cases that look most like case thirteen. Use them to make your estimate, and write your reason down before we reveal the true value.

Writing your reason first matters. Afterwards you can compare what you expected with what was measured, and learn from the difference.

## Slide 30: Reading the pattern from twelve cases

One approach is to compare cases with similar inputs. Follow the steps below.

1

Look down the columns and ask which one seems to move with the outcome. Ignore the others for now.

2

Find the two cases whose value of that column sits either side of case 13's value.

3

Look at their outcomes. Case 13's answer is probably between them.

4

Adjust for anything else you noticed — a second column that also seems to matter.

5

Write the number down, and write why. Then ask: how confident am I, and what would change my mind?

You used a pattern in known examples to predict an unknown value. Comparing that prediction with the measured value tells you how large the error was.

**Spoken script**

Let us read a pattern from the twelve cases. One approach is to compare cases that have similar inputs. Follow the five steps on the slide.

Step one. Look down the columns and ask which column seems to move together with the outcome. Ignore the others for now.

Step two. Find the two cases whose value in that column sits on either side of case thirteen's value. Step three. Look at their outcomes. The answer for case thirteen is probably between them. Estimating between two known points like this is called interpolation, and it is a good guess, though it is never a guarantee.

Step four. Adjust for anything else you noticed, such as a second column that also seems to matter. Step five. Write the number down, write why, and ask how confident you are and what would change your mind.

You have used a pattern in known examples to predict an unknown value. Comparing the prediction with the measured value tells you the size of the error.

## Slide 31: The answer, and your error

The star marks the measured value. Its distance from your prediction is the prediction error. The dashed line shows a possible pattern in the data.

**Spoken script**

Here is the reveal. The chart shows the twelve known cases, and a star marks the measured value of case thirteen.

The distance between your prediction and the star is the prediction error. It is the difference between what you predicted and what was measured. Keep the unit with it, because an error of three is meaningless until we know three of what. If we subtract in the same order each time. In this course we take the measured value minus the predicted value, a positive and a negative error will tell us whether we predicted too high or too low.

The dashed line shows one possible pattern in the data. A line is only one kind of pattern, and other shapes are possible.

One case cannot tell us how reliable a method is. With a single test we only see how it did this once. Later we will use many cases that were held back, and then the error means much more.

## Slide 32: Steps in a prediction task

What you called it

You looked at the table.

You noticed which columns seemed to matter.

You worked out a rough rule in your head.

You applied it to a case you had not seen.

You compared your prediction with the measured value.

What it is called

You explored the data. That is Weeks 5 and 6.

You selected features. That is Week 11.

You proposed a rule. Python models follow in Week 8.

You predicted a value for a case that was not used to find the pattern.

You measured the prediction error. Week 10 covers model evaluation.

**Spoken script**

Now we give names to what you just did. On the slide, the first group lists what you did, and the second group lists what it is called.

You looked at the table. That is exploring the data, which we do in Weeks 5 and 6. You noticed which columns seemed to matter. That is selecting features, in Week 11. You worked out a rough rule in your head. That is proposing a model, and the Python models start in Week 8.

You then applied your rule to a case that you had not seen. That is predicting for a case that was not used to find the pattern. Finally, you compared your prediction with the measured value. That is measuring the prediction error, and Week 10 covers model evaluation.

So on paper, with twelve rows, you went through the same steps that a computer follows later. Nothing was trained today. Later weeks will repeat these steps in Python.

## Slide 33: Break

10 minutes

Take a short break. No computer is needed for the remaining introductory examples.

**Spoken script**

We now take a ten minute break. Stand up, stretch and drink some water.

When we come back, we move to the second half of the introduction. No computer is needed for the remaining examples, and no download or code is required. Come back on time, because we start with the two main kinds of prediction question.

## Slide 34: Two kinds of question

Predicting a number, and predicting a category. Almost everything in this course is one or the other.

**Spoken script**

This is the sixth segment, and it lasts fifteen minutes. We look at two kinds of question. One is predicting a number, and the other is predicting a category. Almost everything in this course is one or the other.

The kind of answer decides the task. If the answer is an amount, such as a torque or a number of days, the task is regression. If the answer is a choice from a list of labels, such as failure or no failure, the task is classification.

Categories can be stored as numeric codes, like zero and one. The digits alone do not decide the task. What matters is what the answer means.

## Slide 35: Regression and classification

Left: the answer is a number on a continuous scale, so we fit a line through the cases. Right: the answer is one of a small set of labels, so we look for a boundary that separates them. The data can be the same; the question is what changes.

**Spoken script**

The slide shows the two shapes. In regression, the answer is a number on a continuous scale. A continuous scale means the value can be any amount between two points, such as any torque between ten and sixty newton metres. To handle this we fit a line or curve through the cases, and we read the prediction from it.

In classification, the answer is one of a small set of labels. To handle this we look for a boundary that separates the labels, so that cases on one side get one label and cases on the other side get the other.

The same data can often support both. If we take a column of measured temperatures, we can predict the temperature itself, which is regression, or we can predict whether it passes a safety limit, which is classification. The data stays the same. What changes is the question we ask, and so the target we choose.

## Slide 36: Regression, and classification

REGRESSION predicts a number on a continuous scale. CLASSIFICATION predicts which of a small number of categories a case belongs to.

Regression: how many % silica? Classification: ore or waste; or lithology: sandstone, shale, limestone.

Ask what the answer means. Estimating a quantity is regression; choosing a category is classification. Categories may use numeric codes.

**Spoken script**

Regression predicts a number on a continuous scale. Classification predicts which of a small number of categories a case belongs to.

For example, a regression question is, how many per cent silica? A classification question is, ore or waste. Another is lithology, which means rock type, such as sandstone, shale or limestone.

To tell them apart, ask what the answer means. Estimating a quantity is regression. Choosing a category is classification. Categories may be stored as numeric codes such as zero and one, but they are still categories.

## Slide 37: Can you answer these?

You want to predict how many days until a component needs replacing. Regression or classification?

You want to predict whether a sample passes or fails specification. Which one?

You want to predict which of five fault types a machine has. Which one — and what makes it different from the previous question?

Answers are on the next slide — try first, then look.

**Spoken script**

Here is another check. Try each one before we show the answers.

Question A. You want to predict how many days until a component needs replacing. Is that regression or classification?

Question B. You want to predict whether a sample passes or fails a specification. Which one is it?

Question C. You want to predict which of five fault types a machine has. Which one is it, and what makes it different from the previous question?

Think about what each answer would look like. Is it a quantity, or is it a choice from a list? The answers are on the next slide.

## Slide 38: How did you do?

Days until replacement?

Regression. The answer is a number with a unit — days.

Pass or fail?

Classification. Two categories, so it is called binary classification.

Which of five fault types?

Still classification, but multiclass rather than binary. Difficulty depends on the data. Week 9 examines which categories are confused, beyond a single accuracy score.

**Spoken script**

Let us see how you did.

For A, days until replacement is regression. The answer is a number with a unit, which is days.

For B, pass or fail is classification. There are two categories, so we call it binary classification. Binary means two.

For C, five fault types is still classification, but it is multiclass instead of binary. Multiclass means more than two categories. A model with more categories is not automatically harder to build. The difficulty depends on how well the categories separate in the data, how many examples we have, and what each error costs.

In Week 9 we study which categories get confused with each other, and that tells us much more than a single accuracy score.

## Slide 39: What machine learning cannot do

Four limitations to consider when using machine learning.

**Spoken script**

This is the seventh segment, and it takes fifteen minutes. We look at what machine learning cannot do. There are four limitations, and we will work through each of them.

A model will always give you an answer. A returned prediction does not prove that the data was good, that a real relationship exists, or that an action is safe. So whenever you see a prediction, the next step is to ask whether the data and the testing really support the use that someone has in mind.

The next two slides give the four limits, first in general terms and then in your own discipline.

## Slide 40: Four limits, and none of them go away

A model can produce a prediction even when the data are unsuitable. Check whether the inputs and evaluation support its intended use.

**Spoken script**

These are four limits of machine learning, and none of them goes away with a better computer.

First, there may be no data, or too few observations. A model can only learn from what has been recorded. Second, the inputs may carry no useful signal. They may be weak or irrelevant to the outcome. Third, a better method may already exist. A known physical equation can beat a model. Fourth, the future may change. Conditions today can differ from the conditions in the past data.

A model can produce a prediction even when the data are unsuitable. It will not warn you. So for every problem, check whether the inputs and the testing support the use you intend.

These four are questions to investigate for each plant and each data set. Each one is a question to investigate in each case.

## Slide 41: The same four limits, in your own discipline

1 · No data

Blast fragmentation was judged by eye for decades. There is no dataset of it.

2 · No signal

The shift supervisor's name does not cause recovery to change. A model given that column will still find a pattern in it.

3 · Physics is better

Contained metal is tonnage times grade. That is arithmetic; there is nothing to predict. Do not use a model where an equation will do.

4 · The future changed

A model trained on one ore body will not transfer to the next bench when the mineralogy changes.

Why this matters for the rest of the course

Every project in Week 9 has to survive these four questions before it is approved. A team that cannot answer them has not defined an engineering problem yet — it has picked a technique and gone looking for somewhere to use it.

**Spoken script**

Here are the same four limits in your own discipline.

One, no data. Blast fragmentation was judged by eye for decades, so there is no data set of it.

Two, no signal. The name of the shift supervisor does not cause recovery to change. A model given that column will still find a pattern in it.

Three, physics is better. Contained metal is tonnage times grade. That is arithmetic, and there is nothing to predict. Do not use a model where an equation will do.

Four, the future changed. A model trained on one ore body will not carry over to the next bench when the mineralogy changes. A bench is one working level of the mine.

This matters for the rest of the course. Every project in Week 9 has to survive these four questions before it is approved. A team that cannot answer them has not defined an engineering problem yet. It has picked a technique and gone looking for somewhere to use it.

## Slide 42: Challenge: the Problem Hunt

Read the problem and identify the information available. Use the worked example to plan your first step.

**Spoken script**

This is the eighth segment, and it takes thirty minutes. It is a challenge called the Problem Hunt.

Your task is to read a problem and identify the information that is available. You then use the worked example to plan your first step. The skill we practise is defining a good question before choosing any technique.

This exercise supports your Assignment A1 brief. It is practice, and it does not create another graded upload. A good answer may even conclude that an established rule is better than machine learning, and that is a perfectly good finding.

## Slide 43: Problem Hunt

List three problems from exploration, ore and reservoir characterisation, production and equipment health where data might help.
Classify each problem: predict a number, predict a category or use another method. Explain your choice.
Use the worked example as a guide. Write down your assumptions and explain your answer.

Work these questions in order

What do you want to predict?

Who measures that, and how often?

Would a rule you already know do this better?

What would the answer let somebody DO?

How would you know if you were wrong?

What does a mistake cost here?

**Spoken script**

This is the Problem Hunt. There are three tasks.

First, list three problems from exploration, ore and reservoir characterisation, production and equipment health where data might help. Second, classify each problem. Is it predicting a number, predicting a category, or something else? Explain your choice. Third, use the worked example as a guide, write down your assumptions, and explain your answer.

Work through six questions in order. What do you want to predict? Who measures that, and how often? Would a rule you already know do this better? What would the answer let somebody do? How would you know if you were wrong? And what does a mistake cost here?

Take one candidate problem and answer all six questions for it. Then repeat the process for the other two.

## Slide 44: How your team works, all semester

Project teams of four or five

You will do two projects together: a data analysis project due Week 8, and the Engineering ML Project from Week 9 to Week 15.

Roles rotate at every milestone

Project roles: data analysis, modelling, engineering review, documentation and presentation. Rotate roles so each member practises different skills.

Individual accountability is built in

Sixty-five per cent of the mark is individual. Your team keeps a contribution log, and it is checked against the repository history.

In Week 15, each student submits an individual written defence and reflection according to the published brief.

Sign the team charter before you leave

Names, contact details, a weekly meeting slot, and what you will do if somebody stops contributing. Agreeing that now is much easier than agreeing it in November.

**Spoken script**

Now let us talk about how your team works all semester. Project teams have four or five people. You do two projects together. The first is a data analysis project, and the second is the Engineering ML Project, which runs from Week 9 to Week 15. The slide gives the due week for the first one.

Roles rotate at every milestone. The roles are data analysis, modelling, engineering review, documentation and presentation. Rotating means each member practises different skills.

Individual accountability is built in. Sixty five per cent of the mark is individual. Your team keeps a contribution log, which is a record of who did what, and I check it against the repository history. The repository is the online folder where your project files and their changes are stored. In Week 15, each student submits an individual written defence and reflection, following the published brief.

Before you leave, sign the team charter. Write the names, contact details, a weekly meeting slot, and what you will do if somebody stops contributing. Agreeing that now is much easier than agreeing it in November.

## Slide 45: Review your examples and Assignment A1

Check your candidate problems, then review A1 and the preparation for Week 2.

**Spoken script**

This is the ninth segment, and it takes ten minutes. We do two things.

First, look again at your candidate problems from the Problem Hunt. Check one of them against the six questions on the earlier slide. Second, we review Assignment A1 and what you need to do to prepare for Week 2.

The next slide explains A1 and the steps before next week. It is written so that someone reading it alone can follow it, so you can return to it when you are revising.

## Slide 46: Before Week 2

Assignment A1 — use the current form deadline

Three candidate machine learning problems from your own discipline.

For each: state inputs, target, data source and one limitation.

Choose one problem and dataset. Explain why it is feasible.

Marks: framing 6, data 8, judgement 6. Submit one DOCX or text PDF.

Also before next week

Create a GitHub account.

Create a Google account if you do not have one — we work in Google Colab from Week 2.

Watch the video on the next slide.

Do NOT install anything.

Week 2 needs a browser only.

Sign and hand in your team charter.

**Spoken script**

Here is Assignment A1, which you complete before Week 2. Use the deadline shown on the course form.

You write about three candidate machine learning problems from your own discipline. For each one, state the inputs, the target, the data source and one limitation. Then choose one problem and its data set, and explain why it is feasible, meaning why it can really be done.

The marks are six for framing, eight for data and six for judgement. Submit one DOCX file or one text PDF.

Also before next week, create a GitHub account, which is a place to store project files online. Create a Google account if you do not have one, because we work in Google Colab from Week 2. Colab lets you write and run Python in a browser. Watch the video on the next slide. Sign and hand in your team charter.

Do not install anything. Week 2 needs only a browser.

## Slide 47: Watch this before Week 2

IBM Technology

AI, Machine Learning, Deep Learning and Generative AI Explained

Runtime: under 10 minutes

Compare the video’s definitions with the diagram in this lesson. Note any terms that the speaker uses differently.

```python
https://www.youtube.com/watch?v=qYNweeDHiyU
```

**Spoken script**

Please watch this video before Week 2. It comes from IBM Technology. Its title is AI, Machine Learning, Deep Learning and Generative AI Explained, and it runs for under ten minutes. The link is on the slide.

As you watch, compare the speaker's definitions with the diagram we used today, where artificial intelligence contains machine learning, and machine learning contains deep learning. Note any terms that the speaker uses differently from us.

Generative AI means systems that create new text, images or other content. We name it here, and we do not study it in Semester 1.

If the video is unavailable, you can use today's slides for the same definitions.

## Slide 48: Revision material

Everything from here on is for you to study from. Summary, self-test with answers, glossary and a one-page reference.

**Spoken script**

This is the tenth segment, and it takes five minutes. Everything from here on is for you to study from.

The slides that follow contain a summary, a self test with answers, a glossary, and a one page reference. Use them in that order when you revise. Attempt the self test first and write something for each question. Only then read the answers. Use the glossary whenever a word is unfamiliar.

These slides recap today's lesson. They do not add any new submission.

## Slide 49: What you should take away

Artificial intelligence is a goal; machine learning is one way of reaching it; data science is the craft of getting a trustworthy answer out of data at all.

In traditional programming you write the rule. In machine learning you supply examples and the computer infers the rule — and you then have to decide whether to trust it.

The supervised tables used here have one row per example, candidate input columns and an observed target. Other datasets can have different structures.

Regression predicts a number with a unit. Classification predicts which of a small set of categories a case belongs to. The same data can pose either question.

A model learns association. It does not learn cause, and a good fit is no evidence of a mechanism.

Check for missing data, weak predictive patterns, better physical models and changes in operating conditions.

A prediction alone does not show that a model is useful. Check the data, errors and limits of the intended use.

**Spoken script**

Let us summarise what you should take away.

Artificial intelligence is a goal. Machine learning is one way of reaching it. Data science is the craft of getting a trustworthy answer out of data at all.

In traditional programming you write the rule. In machine learning you supply examples and the computer infers the rule, and then you must decide whether to trust it.

The tables we used have one row per example, columns of candidate inputs, and an observed target. Other data sets can have different structures, such as images or text.

Regression predicts a number with a unit. Classification predicts which of a small set of categories a case belongs to. The same data can pose either question.

A model learns association. It does not learn cause, and a good fit is no evidence of a mechanism. Check for missing data, weak patterns, better physical models and changed conditions. A prediction alone does not show that a model is useful, so check the data, the errors and the limits of the intended use.

## Slide 50: Self-test — try these before you look

A colleague says 'we should use AI for this'. What three questions would you ask before agreeing?

You have a table of 500 past pump repairs. Which columns are features and which is the target — and what tells you?

Give one problem from your discipline that is regression, and one that is classification.

Why is a very good fit on data the model has already seen NOT evidence that the model is any good?

Your model predicts silica in the concentrate to within a few percentage points. Name one thing you would still need to know before acting on it.

Answers on the next slide. Do not look until you have written something for each.

**Spoken script**

This self test has five questions. Write something for each one before you look at the answers.

Question A. A colleague says, we should use AI for this. What three questions would you ask before agreeing?

Question B. You have a table of five hundred past pump repairs. Which columns are the features, which one is the target, and what tells you?

Question C. Give one problem from your discipline that is regression, and one that is classification.

Question D. Why is a very good fit on data that the model has already seen no evidence that the model is any good?

Question E. Your model predicts silica in the concentrate to within a few percentage points. Name one thing you would still need to know before acting on it.

The answers are on the next slide.

## Slide 51: How did you do?

Three questions before agreeing to 'use AI'?

What value do you want to predict? Which recorded data can help? Is an established equation suitable? Resolve these questions before choosing a model.

Features and target in a repair table?

The target is whatever you want to predict — say time to next failure. Features are everything known BEFORE that: operating hours, load, temperature. The test is timing: anything only known afterwards cannot be a feature.

One of each from your discipline?

Regression: any quantity with a unit — silica in the concentrate in percentage points. Classification: ore or waste; or lithology: sandstone, shale, limestone.

Why is a good fit on seen data not evidence?

A model may memorise its training examples. Evaluate it on separate examples to check whether it predicts new cases well.

What else before acting?

How large the error is in engineering terms and whether that is tolerable; what it costs when the model is wrong; and whether today's conditions still resemble the data it learned from.

**Spoken script**

Here are the answers.

A. Ask what value you want to predict, which recorded data can help, and whether an established equation is suitable. Settle those questions before you choose a model.

B. The target is whatever you want to predict, say the time to the next failure. The features are everything known before that moment, such as operating hours, load and temperature. The test is timing. Anything known only afterwards cannot be a feature.

C. For regression, use any quantity with a unit, such as silica in the concentrate in percentage points. For classification, use ore or waste, or a lithology such as sandstone, shale or limestone.

D. A model may memorise its training examples. To check whether it predicts new cases well, evaluate it on separate examples.

E. You need to know how large the error is in engineering terms and whether that is tolerable, what it costs when the model is wrong, and whether today's conditions still resemble the data it learned from.

## Slide 52: Every word we used today (1 of 3)

Artificial intelligence

Any machine doing something we would call intelligent. A goal that many techniques aim at.

Machine learning

Inferring a rule from examples instead of writing it yourself.

Deep learning

Machine learning using large neural networks. Semester 2.

Data science

The craft of getting a trustworthy answer out of data — finding, cleaning, questioning, analysing, presenting.

Dataset

A collection of data. In this lesson we use tables of observations.

Example (or row, or observation)

One recorded case. A supervised training example includes its observed target.

Feature

A column known before the outcome. An input to the prediction.

Target (or label)

The column you are trying to predict.

**Spoken script**

This is the first of three glossary slides. It lists the words we used today with short definitions.

Artificial intelligence is any machine doing something we would call intelligent. It is a goal that many techniques aim at. Machine learning is inferring a rule from examples instead of writing it yourself. Deep learning is machine learning that uses large neural networks, and it belongs to Semester 2. Data science is the craft of getting a trustworthy answer out of data.

A dataset is a collection of data. In this lesson we use tables of observations. An example, also called a row or an observation, is one recorded case. In supervised learning, an example includes its observed target.

A feature is a column known before the outcome. It is an input to the prediction. The target, also called the label, is the column you are trying to predict.

## Slide 53: Every word we used today (2 of 3)

Regression

Predicting a number on a continuous scale.

Classification

Predicting which of a small set of categories a case belongs to.

Binary classification

Classification with exactly two categories, such as pass or fail.

Multi-class classification

Classification with three or more categories.

Prediction

The model's answer for a case.

Error

Prediction error is the difference between the predicted and measured values.

Unseen data

Cases not used to fit the model. They must also be relevant and free from leakage.

**Spoken script**

This is the second glossary slide.

Regression means predicting a number on a continuous scale. Classification means predicting which of a small set of categories a case belongs to. Binary classification has exactly two categories, such as pass or fail. Multi-class classification has three or more categories.

A prediction is the model's answer for a case. The error is the difference between the predicted value and the measured value.

Unseen data means cases that were not used to fit the model. To be useful, they must also be relevant to the intended use and free from leakage. If you test a model on cases that look nothing like real use, a good score tells you very little.

## Slide 54: Every word we used today (3 of 3)

Data leakage

Accidentally giving the model information it would not have in real use — usually something only known after the outcome. Week 10.

Generalisation

Whether a rule learned from past cases still works on new ones.

Association vs cause

A model learns which columns move together. It knows nothing about mechanism.

**Spoken script**

This is the last glossary slide, with three terms.

Data leakage means accidentally giving the model information that it would not have in real use. Usually that is something only known after the outcome. The repair column from earlier is an example. We return to this in Week 10.

Generalisation asks whether a rule learned from past cases still works on new ones. That is what we really care about.

Association versus cause is the third. A model learns which columns move together. It knows nothing about the mechanism behind them. To show that one thing causes another, you need extra assumptions or a carefully designed study.

## Slide 55: Eight questions to ask about any data problem

1 · What exactly am I predicting?

Name the target column and its unit. A descriptive analysis question may not need a prediction target.

2 · Is it a number or a category?

Does the answer estimate a quantity or choose a category? Numeric class codes are still categories.

3 · What do I know beforehand?

List the features. Check every one: would I really have this before the outcome?

4 · Where does the data come from?

Who measured it, how often, over what period, and is it actually kept anywhere?

5 · Would a rule or an equation do this better?

If a code of practice or a validated formula answers it, use that instead.

6 · How will I know if I am wrong?

You need cases the model has never seen. Decide now how you will hold some back.

7 · What does being wrong cost?

A false alarm and a missed failure are not equally bad. That asymmetry decides which model you pick.

8 · Do today's conditions still resemble the data?

If the process, material or plant has changed, the model may be quietly obsolete.

**Spoken script**

This slide is a cheat sheet with eight questions to ask about any data problem. Keep this slide. You can use it for every project in this course.

One, what exactly am I predicting? Name the target column and its unit. Two, is it a number or a category? Numeric class codes are still categories. Three, what do I know beforehand? List the features and check each one. Would I really have it before the outcome?

Four, where does the data come from? Who measured it, how often, over what period, and is it kept anywhere? Five, would a rule or an equation do this better? If a code of practice or a validated formula answers it, use that.

Six, how will I know if I am wrong? You need cases the model has never seen, so decide now how you will hold some back. Seven, what does being wrong cost? A false alarm and a missed failure are not equally bad, and that decides which model you pick. Eight, do today's conditions still resemble the data? If the process, material or plant has changed, the model may be quietly obsolete.

## Slide 56: Five questions,
five minutes

Features and target read off a table, regression told from classification, and one of the four limits applied to a case.

Enter your own Student Registration Number exactly as recorded.

One attempt, from the Google account you are signed in to.

Open for 24 hours from lecturer activation, then it closes.

Tap View score and read the feedback after submitting.

Quiz category: 10%. Best nine of eleven count; Quiz 6 is waived.

**Spoken script**

The Week 1 quiz has five questions and takes about five minutes. It covers features and target, regression and classification, and one of the four limits applied to a case.

Enter your own Student Registration Number exactly as recorded. You have one attempt, from the Google account you are signed in to. The quiz opens when I activate it and stays open for twenty four hours.

After you submit, tap View score and read the feedback. The quiz category is ten per cent, and your best nine of eleven count because Quiz 6 is waived. Check the slide for the link.

## Slide 57: You have practised
prediction reasoning.

Today you used twelve rows of data to make a prediction and measure its error. Later lessons use Python to repeat these calculations on larger datasets.

Next week: Colab notebooks and version control. Bring a laptop with a browser.

**Spoken script**

The one thing to remember from today is that you have practised prediction reasoning. You used twelve rows of data to make a prediction, and then you measured its error.

Later lessons use Python to repeat these calculations on much larger data sets. The computer does the same kind of work that you did by hand, and it can do it for thousands of rows. Today's paper exercise is not an extra upload.

Next week we start with Colab notebooks and version control. Bring a laptop with a browser.
