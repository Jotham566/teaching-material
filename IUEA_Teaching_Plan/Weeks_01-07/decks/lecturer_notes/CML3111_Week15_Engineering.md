# CML3111 Week 15

Each slide shows its text, then the spoken script the lecturer reads aloud.

## Slide 1: Presenting the project and individual contribution

Communications, Electrical, Mechatronics and Robotics Engineering

Friday 18 December 2026
Friday 11:00–14:00, Room 115

**Spoken script**

Welcome to Week 15, the final week of the course for Communications, Electrical, Mechatronics and Robotics Engineering. Today we present our projects and explain our own contribution to them.

You have spent seven weeks learning to build models and check them honestly. Today is the day to show that work with confidence. Check the slide for your day, time and room.

## Slide 2: Today’s learning

Explain your question and one supported finding.

State a limitation and your individual contribution.

You can point to the evidence behind one decision you personally worked on.

**Spoken script**

Here is what we will do today. We will explain the question our team investigated and one finding that our evidence supports. Then we will state one limitation, which is a place where our evidence is weak or may not apply, and we will say what we personally contributed.

Here is how we will show it. We will be able to point to the evidence behind one decision that we worked on ourselves. That might be a cell in the notebook, a chart, or a result. If you can point to it and explain why you made that choice, you have met today's goal.

This is well within your reach, because you already did the work.

## Slide 3: Connection to the previous lesson

What question did your team investigate, and what result can you support with evidence?

**Spoken script**

Let us connect to the work of the last few weeks. Every week we asked a question of some data, built a model, and checked it carefully.

Now we put that into one story. What question did your team investigate? And what result can you support with evidence?

Take a moment to think about your own project. Try to say the question in one sentence, and then name one result that you could show on the screen. If you can do both, you are already most of the way to a good presentation.

## Slide 4: The continuing pandas workflow

Load CSV files with pd.read_csv. Keep raw data unchanged and use named columns throughout the investigation.

Use pandas for cleaning, summaries and model inputs. Return the published Python types at assessment function boundaries.

**Spoken script**

Pandas is the Python library we have used all course to work with tables of data. We keep using it for the project.

To load a CSV file, which is a plain table saved as text, we write pd dot read underscore csv and give it the file name. We keep the raw data exactly as it arrived. Any cleaning happens on a copy, so we can always go back to the original. We also refer to columns by their names, so that anyone reading our work can follow it.

We use pandas for cleaning, for summaries, and for preparing the inputs to our models. Where the assessment functions have a published return type, such as a float or a list, we return exactly that type. This is revision of what you already know, and it adds no new requirement.

## Slide 5: A presentation connects a claim to evidence

Finding and limitation

A finding states what the evidence shows. A limitation states where that evidence is incomplete or may not apply. Point to the relevant chart, metric or record.

Defence and reflection

A defence explains why you made a choice. A reflection explains what you learned and would improve. Describe your own contribution with specific evidence.

**Spoken script**

A good presentation links what we claim to what we can show.

A finding states what the evidence shows. Suppose the average error on held-out data was 2 deg C. That is an invented example. A limitation states where that evidence is incomplete or may not apply. For example, our sample came from only one site. When we give a finding or a limitation, we point to the chart, the metric or the record that backs it up.

A defence explains why we made a choice. A reflection explains what we learned and what we would improve. In both, we describe our own contribution and give specific evidence for it, such as a named cell or a named chart.

A polished chart helps only when its target, its units and its evaluation sample are clear.

## Slide 6: A six-minute presentation

01

Minutes 1–2: explain the question and data.

02

Minutes 3–4: show the method and one supported result.

03

Minutes 5–6: explain limitations, contributions and a next step.

**Spoken script**

Your presentation lasts six minutes, so we split it into three parts of two minutes each.

In the first two minutes, we explain the question and the data. What engineering problem did we look at, and what data did we use?

In minutes three and four, we show the method and one supported result. We choose one result that we can back with a chart or a number, and we explain how we obtained it.

In the last two minutes, we explain the limitations, who contributed what, and a sensible next step. Planning the time this way keeps us calm, and it means we do not run out of time before reaching the honest part about limitations.

## Slide 7: Make the evidence readable

01

Name the chart axes and their units.

02

State the measured evaluation result and how you obtained it.

03

Point to the particular table, plot or calculation that supports your claim.

**Spoken script**

Evidence only helps if the audience can read it. Three habits make it readable.

First, we name the chart axes and their units. If the vertical axis shows error, we say it is error in kilowatts, or whichever unit our target uses.

Second, we state the measured evaluation result and how we obtained it. For example, we say which metric we used, and that it was measured on data the model had not seen during training.

Third, we point to the particular table, plot or calculation that supports our claim. We say which one it is and we show it. When the audience can see exactly where a claim comes from, they can trust it.

## Slide 8: Limitations of the results

01

State what your investigation can support.

02

If an answer is unknown, say what evidence would resolve it.

03

Teaching data alone do not establish readiness for real operation.

**Spoken script**

Every project has limits, and stating them clearly is a strength.

First, we state what our investigation can support. Perhaps our model predicts well on the sample we tested, and we say so plainly.

Second, if there is something we do not know, we say what evidence would answer it. For example, if we do not know whether the model works at a new site, we say that data from that site would tell us.

Third, we remember that teaching data alone do not show that a model is ready for real operation. Real equipment, real weather and real people bring conditions our data may not include. Saying this honestly shows engineering maturity and earns the audience's trust.

## Slide 9: Preparation checkpoint

Each student can explain one decision they personally worked on and point to its evidence.

**Spoken script**

Here is a checkpoint to prepare with. Each of us should be able to explain one decision we personally worked on and point to its evidence.

Choose your decision now. It might be how you handled missing values, how you split the data, or why you chose a particular metric. Find the cell, chart or entry in the contribution log where it appears.

Then prepare three short things to say. What did you decide? Why did you decide it? What is one limitation of that choice?

Talking about this today is practice, and nobody is being graded on it live. The marks come from the written evidence you submit.

## Slide 10: Your evidence

01

Use the published project and DEMO requirements.

02

Each individual submits their own typed defence and reflection through the designated route.

03

Submit your own written defence and reflection as instructed.

**Spoken script**

There are two kinds of evidence in this final stage. The team project is one. Your own individual defence and reflection is the other, and they have separate purposes.

First, use the published project and DEMO requirements. These list exactly what is needed, so read them before you finish.

Second, each of us submits our own typed defence and reflection through the designated route. A defence points to specific cells or results in the project. A reflection describes how our understanding changed.

Third, we write these ourselves and submit them as instructed. A single team reflection copied for everyone does not show what you personally learned, so please write your own.

## Slide 11: Engineering ML project

01

Write your own explanation in the markdown cell headed `## My written evidence`.

02

Keep that heading.

03

Task prompts and code comments are excluded from reasoning marks.

04

Complete every original rubric criterion below, not just the checked functions.

**Spoken script**

Now we look at what the project marking expects in the notebook.

First, write your own explanation in the markdown cell headed hash hash My written evidence. A markdown cell is a notebook cell that holds ordinary text.

Task prompts and code comments are excluded from the reasoning marks. This means the marks for reasoning come from your own sentences. Explain your choices in your own words, and connect each one to a result and its limitation.

Finally, complete every original rubric criterion shown on the next slides. Do not stop after the functions that are automatically checked, because the rubric covers the whole project.

## Slide 12: Engineering ML project continued

01

Include profiling, justified cleaning, question-led charts and your engineering recommendation where required.

02

Keep raw data.

03

State units and distinguish correlation from causation.

04

Charts must be actual labelled figures in the notebook, not claims that charts exist.

**Spoken script**

Here is the next group of project requirements.

Include profiling, which means a first careful look at the data to see its columns, types and gaps. Include cleaning that you can justify, charts that answer a stated question, and your engineering recommendation, where the rubric asks for them.

Keep the raw data untouched. State units wherever you give a number. And take care to separate correlation from causation. Two things moving together does not show that one causes the other.

Finally, charts must be real, labelled figures in the notebook. Writing a sentence that says a chart exists will not earn the marks. The chart itself must appear, with labelled axes.

## Slide 13: Engineering ML project continued

01

Include captions and a separate readable DOCX/PDF report.

02

Problem definition (15.0 total): The engineering problem is real, specific and bounded.

03

The ML task is correctly derived from it.

04

The target variable is justified, not merely available.

**Spoken script**

Next we look at the first marking criterion, and a few related requirements.

Include captions on your charts, and a separate readable report as a DOCX or PDF file.

Problem definition carries fifteen marks in total. The engineering problem should be real, specific and bounded. A broad theme such as AI for buildings is too wide. Name the decision, the users and the setting.

The machine-learning task should follow correctly from that problem. If the decision needs a number, the task is regression. If it needs a category, the task is classification.

And the target variable, which is the thing we predict, should be justified. We choose it because knowing it helps the decision, and its mere presence in the file is not a good enough reason.

## Slide 14: Engineering ML project continued

01

Data understanding (15.0 total): Provenance, licence and collection method stated.

02

Defects found and handled with justification.

03

Limitations of the data acknowledged before any modelling.

04

Methodology (20.0 total): Appropriate models chosen and compared under one protocol.

**Spoken script**

This slide covers two criteria.

Data understanding carries fifteen marks in total. State where the data came from, which is its provenance, what licence allows you to use it, and how it was collected. If the data are synthetic, say so.

Then show the defects you found, such as missing values or impossible readings, and handle each one with a reason. Acknowledge the limitations of the data before any modelling begins, so the reader knows what to be careful about.

Methodology carries twenty marks in total. Choose appropriate models and compare them under one protocol. That means the same split, the same metric and the same preparation rules for every model. A fair comparison lets the reader trust which model is better.

## Slide 15: Engineering ML project continued

01

Pipeline used.

02

Hyperparameters handled sensibly.

03

Choices explained rather than defaulted to.

04

Engineering reasoning (20.0 total): Domain knowledge visibly enters the work through features, banding, metric choice or interpretation.

**Spoken script**

Let us finish the methodology criterion and then move to engineering reasoning.

Show the pipeline you used. A pipeline chains preparation steps and the model into one ordered process, so the steps run the same way every time. Handle hyperparameters sensibly. Those are settings, such as tree depth, which we choose before training. And explain your choices. Each default you accepted or setting you changed should have a short reason.

Engineering reasoning carries twenty marks in total. Here the marker looks for domain knowledge visibly entering the work. It can enter through the features you built, through how you grouped values into bands, through the metric you picked, or through how you interpret the result. Your engineering training is exactly what makes your project stronger than a generic one.

## Slide 16: Engineering ML project continued

01

The result is discussed as engineering, not as a score.

02

Validation (15.0 total): Correct train/test discipline, cross-validation with a reported spread, leakage explicitly checked and ruled out, metric justified against the cost of error.

03

Communication (10.0 total): The 2-page brief is readable by a non-specialist engineer.

**Spoken script**

Now two more criteria.

First, we discuss the result as an engineering finding. We say what it means for the decision it supports, and we go beyond quoting a score.

Validation carries fifteen marks in total. Keep correct train and test discipline, so the test data stay untouched until choices are fixed. Use cross-validation, which repeats the train and test process on different parts of the data, and report the spread of the results across those repeats. Check for leakage explicitly and show that you ruled it out. Leakage means information from outside the training data slipped into the model. And justify the metric against the cost of error.

Communication carries ten marks in total. Your two-page brief must be readable by a non-specialist engineer, so keep the language plain.

## Slide 17: Engineering ML project continued

01

Charts answer questions and are captioned with findings.

02

State uncertainty and limitations.

03

Reproducibility & documentation (5.0 total): Repository runs from a clean clone.

04

README complete. requirements.txt present.

**Spoken script**

Here are the last few requirements, which cover charts, honesty and reproducibility.

Charts should answer questions, and each should have a caption that states the finding. Also state your uncertainty and your limitations plainly.

Reproducibility and documentation carries five marks in total. Your repository should run from a clean clone. That means someone who downloads a fresh copy of the project should be able to run it and get the same results. The README, which is the project's instruction page, should be complete. And a requirements dot txt file should be present, listing the libraries the project needs.

These five marks reward careful housekeeping, and you can secure them with a final check before you submit.

## Slide 18: Engineering ML project continued

01

Seeds set.

02

AI use declared.

03

Contribution log present.

**Spoken script**

Three last items complete the rubric.

First, seeds should be set. A seed fixes the starting point of the random choices in our code, so a rerun gives the same results as the first run.

Second, declare your AI use. We will look at what a good declaration says in a moment.

Third, include a contribution log. This records who produced and explained which work. Make the entries specific. Name a file, a function or a chart, and the decision behind it, and make sure it matches the history in the repository.

These items support your analysis and sit alongside it.

## Slide 19: Engineering ML project submission

01

Opens: 27 Nov 2026, 11:00 Kampala

02

Deadline: 18 Dec 2026, 11:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open ML_PROJECT assignment form

https://docs.google.com/forms/d/e/1FAIpQLSeV2_XlDSjUCyjJG-aQjFSQny-ndfkYaOYtExv9CdA_HUbDlQ/viewform

**Spoken script**

This slide is where you hand in the Engineering ML project. Check the slide for the opening time and the deadline, and use the form link on the slide.

Enter your full Student Registration Number in the form. Upload the completed project notebook together with your readable report.

Keep a copy of the submitted files and your confirmation. A file saved in Drive or GitHub is not a submission until it has gone through the form.

## Slide 20: Presentation evidence (35 marks)

01

Slides and narration notes explain the question, method, evidence and limitations for an engineering audience.

02

The local text grader does not assess visual styling or spoken delivery.

**Spoken script**

The presentation evidence carries thirty-five marks. Your slides and your narration notes should explain the question, the method, the evidence and the limitations, written for an engineering audience.

Narration notes are the words you would say with each slide. Write them so that someone reading the file alone, without hearing you speak, can follow the whole story from the question to the limits.

The local text grader reads text only. It does not assess visual styling or how you deliver the talk. So put the reasoning in actual text, and avoid leaving it only inside screenshots. For a results chart, the notes should name the sample, the target unit, the metric and what the result means.

## Slide 21: Individual written defence (40 marks)

Two typed answers about the student's own repository identify specific cells/results and explain the decisions.

Credit is based on the submitted evidence; live questioning is formative.

**Spoken script**

The individual written defence carries forty marks, the largest part of the individual evidence.

You write two typed answers about your own repository. In each answer, you identify specific cells or results and explain the decisions you made.

A strong answer links a choice, a reason and a piece of evidence. For example, we might write that we used a group split because the same equipment appears repeatedly, and that a particular cell lists equipment identifiers with no overlap between the groups. A general definition of group splitting does not show that your project used it, so always point to your own work.

Credit comes from the evidence you submit. Live questioning is formative, which means it is there to help you learn and is not marked.

## Slide 22: Reflection (20 marks)

01

500 words.

02

Specific about what changed since Week 1, what remains difficult, and two concrete Semester 2 goals.

03

Generic reflection scores low.

**Spoken script**

The reflection carries twenty marks. It is 500 words, and it is a chance to look back on how far you have come.

Make it specific in three ways. Describe what changed in your understanding since Week 1. Say what remains difficult for you. And give two concrete goals for Semester 2.

For example, you might describe a mistake in the order you ran notebook cells, how running the whole notebook from the top revealed it, and how you now check for it. A goal could be to practise grouped validation on a second dataset.

A sentence such as I learned a lot about AI gives the marker little to work with, and generic reflections score low. Your honest, particular story will score well.

## Slide 23: AI-use declaration (5 marks)

Present, complete and plausible against the repository history.

**Spoken script**

The AI-use declaration carries five marks. It must be present, complete, and plausible when compared with your repository history.

A good declaration is informative. It names the tool, the task it helped with, the file or section affected, and how you checked the output. If you used no AI at all, say that directly.

Disclosure records the help you received. You remain responsible for everything you submit, and you must be able to explain your own work. Always follow the policy for the particular assessment you are completing.

## Slide 24: Presentation and individual reflection submission

01

Opens: 27 Nov 2026, 11:00 Kampala

02

Deadline: 18 Dec 2026, 14:00 Kampala

03

Use your full Student Registration Number in the form.

04

Keep the submitted files and confirmation.

Open DEMO assignment form

https://docs.google.com/forms/d/e/1FAIpQLScnSPyvzCLfoHhIBusvFTIpqC-zAsk2bCLMqu6kJCh5cGI9gQ/viewform

**Spoken script**

This slide is where you hand in the presentation and your individual reflection. Check the slide for the opening time and the deadline, and use the DEMO form link shown.

Enter your full Student Registration Number. Upload your presentation with its narration notes, and your written defence and reflection document, as in the published project and DEMO requirements. Wait for the file names to appear, then press Submit.

Keep the submitted files and the confirmation. A file saved in Drive or GitHub is not a submission until it has gone through the form.

## Slide 25: Revision and submission checklist

You can point to the evidence behind one decision you personally worked on.

Check that the required files are in place.

Point to your evidence. Save your work.

**Spoken script**

Let us finish with a short exit check. Ask yourself whether you can point to the evidence behind one decision you personally worked on. If you can name the cell or chart, say why you chose it, and give one limitation, you are ready.

Then save your work and check the required submission files. Make sure you are uploading your own saved project files, and read the live form for the current requirements.

You have learned a great deal this semester, and this is your chance to show it. Well done, and good luck.
