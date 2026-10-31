# Review and curriculum rationale

Reviewed 26 September 2026. The earlier ML-only syllabus is retained as a historical reference; it is not the launch brochure.

## Changes made

- Added school leavers awaiting university and a separate 24-session Data Analysis path. Each pathway has a distinct final product and starts without prior coding, spreadsheet or statistics assumptions.
- Replaced the claim that learners already have all relevant A-level mathematics with explicit mean, median, range, proportions and model-error teaching.
- Removed the crowded clustering/neural-network week from the core ML promises. Core models are a linear regression and a small decision tree, compared with simple baselines. Advanced AI is a later pathway, not an eight-week mastery claim.
- Introduced project questions in Week 4 and reserved Weeks 7 and 8 for building, checking, explaining and demonstrating. Project preparation accumulates earlier through checkpoints.
- Replaced a class survey designed for about 25 rows with supplied synthetic practice records. A five-person group cannot supply the old assumed dataset size; even names-free combinations could identify students. Students are not required to publish personal surveys.
- Corrected the impression that penguins and house-price datasets all ship inside scikit-learn. This pack supplies its synthetic CSVs and uses the documented bundled iris dataset.
- Removed universal sample-size claims such as 40 rows being sufficient or 200 guaranteeing validity. Data size affects uncertainty; the exercises teach the workflow and its limitations.
- Removed unsupported university-course equivalence, exam-improvement claims and implied vendor/university endorsement. Certificates identify the programme and demonstrated work, not accreditation.
- Replaced compulsory public GitHub portfolios with local/private project copies. Google, GitHub and generative AI accounts are not prerequisites. No age-rule workaround is suggested.
- Made group pricing precise. Three/four-person prices, venue, duration and dates still require the organiser's decision. Marketing has no invented payment destination or scarcity claim that places are already sold.

## External benchmarks and how they are used

These are curriculum references, not endorsements or partner organisations. Do not place their logos or certificates on the marketing material.

1. Google Data Analytics certificate overview: https://grow.google/certificates/data-analytics/ . Used to benchmark the question-to-data-to-analysis-to-communication workflow. The revised DA camp uses Python, pandas, NumPy, matplotlib and seaborn; it adapts the workflow without promising the entire professional certificate or job readiness.
2. DeepLearning.AI Machine Learning Specialization overview: https://www.deeplearning.ai/specializations/machine-learning . Used to benchmark foundational prediction concepts. The camp adds a longer zero-code entry ramp and excludes advanced neural networks and unsupervised methods from its core outcomes. The overview search result was available; the alternate course URL returned 403 during review.
3. Raspberry Pi Foundation AI education: https://www.raspberrypi.org/teach/ai-education . Used to benchmark age-appropriate AI literacy, practical experience and critical evaluation. The camp's lesson text, examples, worksheets and artwork are original; third-party lessons are not reproduced in the paid pack.
4. Jupyter installation: https://jupyter.org/install . Official installation reference for the instructor-prepared local notebook environment.
5. seaborn: https://seaborn.pydata.org/tutorial/introduction.html . Statistical charts on top of matplotlib and pandas, used in the exploration sessions.
6. LibreOffice: https://www.libreoffice.org/download/ . Optional Writer/Impress tools for reports and presentation slides. Calc/Excel is not the DA analysis tool.

## Teaching design

Every lesson has a prerequisite, explicit definitions, a worked example, expected output, independent task and a specific error-repair cue. The instructor pack keeps answers separate. Each student changes an example, explains the change and submits individual evidence. Task progress is based on understanding, not copying fast.

The materials and code checks are a preparation pack, not evidence of a completed learner pilot. Device compatibility, teaching time and learner comprehension should be verified with the actual delivery setup before launch. Public marketing should be finalised with the organiser's branding and booking arrangements.

## September 26 update and explicit benchmark mapping

References reviewed: [Google Data Analytics](https://www.coursera.org/professional-certificates/google-data-analytics), [IBM Machine Learning](https://www.coursera.org/professional-certificates/ibm-machine-learning), [roadmap.sh Data Analyst](https://roadmap.sh/data-analyst), [roadmap.sh AI and Data Scientist](https://roadmap.sh/ai-data-scientist).

Google’s beginner certificate follows questions, preparation, cleaning, analysis, visual communication and a case study. Its current page lists Python and Tableau and a six-month estimate at ten hours/week. The DA camp adapts that workflow through Python, pandas, NumPy, matplotlib, seaborn and a small individual investigation; it does not reproduce the full certificate. Python analytics is core. Tableau/Power BI, SQL and spreadsheet specialisation remain later study and are not camp outcomes.

IBM’s ML course descriptions expect Python and mathematics including statistics, probability, linear algebra and calculus. Its regression, classification, unsupervised and deep-learning coverage is broader than this beginner camp. Camp ML01–12 and F01–04 build the entry bridge; ML13–18 teach baseline comparison, regression, classification and evaluation; ML19–24 apply them to a project. Unsupervised learning, deep learning, formal calculus and advanced linear algebra remain later study. F04 introduces slope intuition only. Passing this camp does not establish readiness for every IBM module.

The roadmap.sh pages reinforce starting with data/programming/statistics, practising on small projects and communicating findings. DA01–12 build Python, pandas, cleaning and charts; DA13–18 add NumPy, seaborn exploration, cleaning a raw export and merging tables; DA19–24 provide a project. ML uses the analogous preparation → model → evaluate → explain progression. These are selected learning directions, not a claim that every node of either career roadmap is covered.

Four additional two-hour ML labs are the recommended timetable revision, not a claim that eight extra hours guarantee mastery. Use individual readiness checks and adapt pace. DA retains three classes/week. Both tracks require the learner’s own laptop. No paid vendor subscriptions or vendor certificates are included. Fees remain unchanged; exact dates, session lengths, venue and booking terms need organiser confirmation before bookings.

## Python-first correction

The organiser clarified that DA teaches Python for data analysis. The former spreadsheet-first interpretation has been replaced throughout the active curriculum, marketing, setup, rubrics and ZIP. Both tracks share Python foundations; DA proceeds to descriptive and exploratory analysis, while ML proceeds to predictive modelling. Existing independent freelance DataAnalysis_Track materials are a separate programme. The pasted external marketing review is feedback, not authority to change fees, doctoral status, prerequisites or promise real-world datasets: supplied camp data remains explicitly synthetic.

## Revision 2 (31 October 2026)

An independent review of the pack (see Schools_ML_Track/docs/Camp_Restructuring_Proposal.docx) found that the two tracks shared identical text for ten of their first eleven sessions; that session 7 asked for about eighteen new words in one sitting; that the SQL sessions gave one worked statement each on a 60-row, three-product table, in a separate tool; that the first machine learning model appeared in session 13; and that every sheet and guide used one template. NumPy and seaborn appeared in no lesson, and means and medians were taught with the standard-library statistics module.

Changes: every session now has one question, at most six words with an everyday comparison, two 50-minute predict-run-investigate-modify blocks, an error card and an exit ticket. SQL moved to the professional courses and the track was renamed Python for Data Analysis. NumPy and seaborn entered both tracks. Machine Learning gained a run-first prediction in session 1, a hand-written flower rule in session 4, a lighter session 7, NumPy in labs F02 to F04, plot_tree and ConfusionMatrixDisplay, a noisy fares dataset with a deliberate leakage column, and an optional extension. The Sunrise Shops dataset (generated, seeded, with an answer key and 32 independent checks) replaces the 60-row table after week 2.

Sources used for the design, read as search-result summaries only because page fetching was not available in the review session. Check each at the source before quoting a figure to parents.

- PRIMM (Sentance, Waite and Kallia 2019): https://computingeducationresearch.org/projects/primm/ . Predict, Run, Investigate, Modify, Make. A quasi-experiment with 493 PRIMM students against 180 comparison students reported a post-test advantage.
- Margulieux, Catrambone and Guzdial 2016 (subgoal-labelled worked examples), Ericson et al. (Parsons problems, CHI 2021 and Koli Calling 2017), Becker (enhanced error messages), Bootstrap:Data Science (https://www.bootstrapworld.org/), Kaggle Learn Pandas (https://www.kaggle.com/learn/pandas).
- TensorFlow installation page: https://www.tensorflow.org/install/pip . Other pages disagree on supported Python versions, so preflight before any use.

Not established: no beginner pilot has been run, no source compares these designs for teenagers, and nothing here measures comprehension. The order of weeks 5 and 6 is an inference to test in a pilot.
