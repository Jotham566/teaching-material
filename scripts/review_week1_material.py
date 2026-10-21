"""Slide-specific Week 1 notes and narrow corrections, retaining original artwork."""
import json,zipfile,xml.etree.ElementTree as E,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review/2026-10-20/full-course-review';A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
NOTES={
1:'Begin with a decision engineers make: estimate a quantity or identify a condition from observations. Today introduces the ideas using the embedded tables and illustrations; no CSV download or Python is needed. A prediction is an estimate, not proof that an action is safe.',
2:'Introduce the tutor’s applied data work briefly. The formal status is incoming PhD student in Applied Informatics at Osaka Metropolitan University, Japan, for April 2027; enrolment has not started. The examples illustrate different applications, not identical model architectures.',
3:'Read the outcomes as questions learners should be able to answer by the end. Start with AI and machine learning in ordinary language; features, targets and task types are introduced later. Learners do not need those terms beforehand.',
4:'Explain the lesson’s sequence: define the ideas, inspect a worked example, then practise identifying a sensible prediction task. Timings are a guide, not a requirement to rush. The activities can be completed individually.',
5:'Follow the semester from setup and Python to tables, cleaning, practical tests and models. Weeks 7 and 14 are test weeks. Test-day downloads and Colab submission follow the current test-entry instructions; do not substitute older offline-test guidance.',
6:'Connect each course goal to visible evidence: a runnable notebook, a correct summary, a reasoned chart or an evaluated model. Knowing a tool name is not the same as explaining a result. Engineering meaning and units remain part of every calculation.',
7:'Introduce how individual work and projects fit together. The next assessment slide supplies the components and weights. Separate weekly tasks from project milestones so students do not confuse one submission with another.',
8:'Walk through the displayed assessment components and add their weights to 100%. Explain which work is individual and which is a project. The current cohort waiver policy overrides old weekly counts: All three programmes have A6 and Quiz 6 waived, including earlier CML3111 submissions. Waived tasks do not become zeros.',
9:'Explain reproducible work as work another person can rerun from the supplied files and instructions. Students should state sources, units and contributions. Asking for help is useful when the learner can show the attempted step and the exact error.',
10:'This is a map of later topics, not an instruction to learn them all today. A roadmap puts tools and ideas in order. Distinguish the topics taught this semester from those deferred to Semester 2.',
11:'Follow the highlighted route from Python to data preparation and evaluation. Explain that a roadmap is a curriculum outline. Neural networks and transformers are later topics; no understanding of their internal mathematics is assumed here.',
12:'Connect each foundation to its purpose. Arithmetic expresses measurements; statistics summarises variability; vectors and matrices arrange inputs; programming repeats a calculation. The course introduces the required operations before its worked examples.',
13:'Read the coverage boundary literally. Topics outside the highlighted route are not hidden prerequisites for weekly work. Explain MLOps only as operating and monitoring deployed models; the full subject is outside this course.',
14:'Different roles emphasise different work: analysis explains data, data science investigates questions, ML engineering implements prediction systems, and data engineering supplies reliable data. The course builds introductory skills, not an immediate professional qualification.',
15:'Move from job titles to the engineering question shown next. Start with the decision and available observations. Choosing a model before defining the question can produce an impressive score that does not help anyone.',
16:'Explain the nested picture: machine learning is an approach within AI; deep learning is a family within machine learning. Data science overlaps these but also includes finding, checking, summarising and explaining data without training a model.',
17:'AI is the broad area of systems performing tasks associated with intelligence. A fixed rule can be part of an AI system; AI does not always mean learning. Avoid implying that the system understands a problem as a person does.',
18:'A learning algorithm uses examples to adjust a model’s settings. We still choose the question, inputs and evaluation. The computer does not automatically discover a valid engineering law or decide whether its own prediction is safe.',
19:'Data science begins before modelling and continues after it. For example, counting missing sensor readings, checking units and explaining a trend are data-science work even if no predictive model is built.',
20:'Contrast a hand-specified rule with a rule fitted from examples. Both take inputs and produce an output; what differs is how the mapping is obtained. An established equation can be the better option when its assumptions apply.',
21:'Identify the outcome, the information available beforehand, and the time at which a prediction would be useful. If an input is known only after the outcome, it cannot support that advance prediction. The following paper example illustrates the reasoning with small embedded data.',
22:'Trace the diagrams left to right. In conventional programming, a person supplies the rule. In supervised learning, past inputs and observed outcomes help an algorithm fit a rule. Then that fitted rule predicts outcomes for new inputs. Do not assume students have programmed before.',
23:'Explain the decision criteria one by one. Known equations still require valid units and assumptions. Learning from examples requires enough relevant data and evaluation on separate cases. Interpretability is a requirement to examine, not proof that every learned model is unexplainable.',
24:'Point to one complete row: it represents one observation. Read its column names and units before using any numbers. Identify candidate inputs available at prediction time, then the outcome to predict. The embedded table is the learning aid here; it is not a file students must locate.',
25:'A feature is an input chosen for prediction; the target is the answer being predicted. Not every earlier measurement is useful, and an identifier may be only a label. Association means two quantities vary together; it does not establish that changing one causes the other.',
26:'Let students identify the target and exclude the post-outcome repair information. The reason is timing: information unavailable when predicting would leak the answer. A valid fixed formula is an acceptable alternative to ML. The next slide explains these answers.',
27:'Explain why the target is the requested outcome, not simply the last column. The repair-after-failure column is excluded because it would not be available beforehand. For electrical examples, Ohm’s law is V = IR; DC electrical power is P = VI. They are different relationships with different assumptions.',
28:'Use the twelve embedded observations as known examples. Case 13 is withheld from the pattern-finding step. This is an individual paper exercise to practise prediction reasoning; it is not a requirement to write or train a model yet.',
29:'Read the table’s headings and units first. Select similar known cases, make an estimate for case 13 and record a reason before the reveal. There is no requirement to form a team in class. The goal is an explained estimate, not guessing the exact measured answer.',
30:'Work through the five visible steps using the actual table. Interpolation estimates between neighbouring observations; it does not guarantee that the outcome lies between theirs. Explain why a second input may matter. Keep a record of the estimate before showing the measured outcome.',
31:'Read the star as the withheld observation and compare it with the previously recorded estimate. State the chosen signed-error convention before subtracting, and retain the measurement’s unit. Absolute error measures size without direction. One held-out case is not enough to establish reliable performance.',
32:'Map the paper actions to later computing steps without claiming a computer was trained today. Looking at patterns is exploration; choosing columns is feature selection; an algorithm later fits model parameters. Separate evaluation asks whether the fitted rule works on observations it did not learn from.',
33:'Pause before introducing task types. No code or download is required for the second half of this introductory lesson.',
34:'Explain that the kind of answer determines the task. An estimated amount is a regression target; a choice among categories is classification. Categories can be represented by numeric codes such as 0 and 1, so digits alone do not determine the task.',
35:'The line is one possible regression model, not the definition of regression. Curved relationships are also possible. The boundary illustrates classification; it separates predicted categories. The same inputs may support different tasks depending on the target we define.',
36:'Ask what the output means, not only how it is written. A quantity such as torque or days is regression; a class such as failure/no failure is classification. A label encoded as 0 or 1 is still a category. Regression can also predict quantities without physical units.',
37:'Days until replacement is a numerical quantity. Pass/fail has two classes. Five fault types give multiclass classification. Identify the target meaning before choosing a method; students can answer without knowing a model algorithm.',
38:'Explain binary as two categories and multiclass as more than two. More classes do not automatically make every dataset harder; difficulty also depends on their separation, examples and error costs. A confusion table will later reveal which categories are mixed up.',
39:'Introduce four reasons a prediction may not be useful. A model returning an answer is not evidence of data quality, a real predictive relationship or safe operation.',
40:'Walk through the four limits on the diagram: inadequate observations, weak or irrelevant inputs, a better known equation, and changes between past and current conditions. Explain that these are questions to investigate rather than universal claims about every plant or dataset.',
41:'Treat each engineering situation as an illustrative scenario. Missing historical observations prevent learning that relationship from those observations. A superficially correlated label may fail elsewhere. A validated physical equation can be preferable. Changed equipment or materials can invalidate an old evaluation.',
42:'Introduce the Problem Hunt as practice defining a question before choosing a technique. It supports the A1 brief; it does not create another graded upload.',
43:'Work through one candidate: specify the outcome, potential measurements, who records them, the decision helped and the cost of error. Then identify two other candidates. A good answer may conclude that an established rule is better than ML.',
44:'Project teamwork is separate from today’s individual exercises. Explain rotating roles and the contribution log as specific records of who produced and explained each part. Individual written defence and reflection follow the current Week 15 brief; do not promise an unannounced live examination.',
45:'Review one candidate problem against the visible questions, then explain the A1 submission checklist. Do not require a gallery walk or peer boards. The assignment should be understandable to someone revising alone.',
46:'A1 asks for one report covering three candidate problems and a justified choice of one. For each, identify inputs, target where appropriate, a possible data source and a limitation. Use the current form deadline. Account setup is preparation for Week 2, not a second report.',
47:'The video is supplementary. Ask students to compare its definitions of AI, ML and deep learning with the lesson. Preview it before class; availability and suggested excerpt timings may change. Students can use the preceding explanations if the video is unavailable.',
48:'Explain how to revise: attempt the self-test before reading its answers, then use the glossary to clarify unfamiliar terms. The reference slides summarise this lesson; they do not introduce additional submission requirements.',
49:'Recap the chain: engineering question, suitable observations, candidate inputs and target, method choice, evaluation and limitations. The row-and-column description applies to the supervised tables used here, not every possible dataset. Images, text and unlabelled data can have other structures.',
50:'Students should justify each answer. Features depend on what is known at prediction time. A score on training data can reflect memorisation. Before acting on a prediction, examine the error tolerance, operating conditions and consequences of mistakes.',
51:'Use each answer to explain the reason. The target is determined by the question. Candidate features must be available beforehand and then checked for usefulness. Separate evaluation tests generalisation, but also needs relevant cases and protection against leakage.',
52:'Define the terms in the context of today’s table. A dataset is a collection of data; it need not always be a table. An observation is one case; a target is needed for a supervised labelled example but may be missing for a new case awaiting prediction.',
53:'Differentiate prediction, observed value and error. Binary and multiclass refer to the number of categories, not to how category labels are stored. Unseen cases must also be relevant to intended use; an unrelated held-out set is not automatically a fair evaluation.',
54:'Give a timing example for leakage: a repair recorded after failure is unavailable when predicting failure. Generalisation concerns new cases. Association alone does not establish causation; causal conclusions need additional assumptions or study design.',
55:'Use the eight questions as a decision checklist. A prediction task needs an outcome, but descriptive data analysis can answer questions without a target. Check availability, evaluation and consequences before committing to a model.',
56:'Explain the difference between estimated completion time and availability: the quiz may take about five minutes, while its response window is 24 hours from lecturer activation. Use the cohort’s current quiz policy and the active link. The course’s quiz category remains 10% even where Quiz 6 is waived.',
57:'Close accurately: today learners practised reasoning from observations, making a prediction and checking error. Later Python lessons fit and evaluate models computationally. Bring a laptop and browser for Week 2; the introductory paper example is not an extra upload.'}
REPLACE={
'You have already done':'You have practised',
'machine learning once.':'prediction reasoning.',
'Stretch, and talk to someone you have not worked with. Nothing after the break needs a computer.':'Take a short break. No computer is needed for the remaining introductory examples.',
'What would the answer look like written down? A quantity with a unit means regression; a word means classification.':'Does the answer estimate a quantity or choose a category? Numeric class codes are still categories.',
'On the left, the way you already know:':'On the left, a rule specified by a person:',
'Everything measured beforehand is a feature.':'Measurements available beforehand are candidate features.',
'Every dataset has the same shape: one row per example, feature columns known beforehand, one target column you want to predict.':'The supervised tables used here have one row per example, candidate input columns and an observed target. Other datasets can have different structures.',
'Power is voltage times current. Do not train a model to rediscover Ohm\'s law.':'For DC circuits, power is voltage times current. Ohm’s law is voltage = current × resistance.',
'TEAM TASK · 15 MINUTES':'INDIVIDUAL PRACTICE · 15 MINUTES',
'Gallery walk, and what you owe me':'Review your examples and Assignment A1',
"Critique two other teams' boards, then the assignment and the pre-work for next week.":'Check your candidate problems, then review A1 and the preparation for Week 2.',
'You have already done\nmachine learning once.':'You have practised\nprediction reasoning.',
'You fitted a model. That is Week 8.':'You proposed a rule. Python models follow in Week 8.',
'Each other. Ask \'what would the answer look like written down?\' A quantity with a unit means regression. A word or a label means classification.':'Ask what the answer means. Estimating a quantity is regression; choosing a category is classification. Categories may use numeric codes.',
'A table of past cases you can learn from.':'A collection of data. In this lesson we use tables of observations.',
'One case: all its features plus its known outcome.':'One recorded case. A supervised training example includes its observed target.',
'Cases the model was not shown while it was learning. The only fair test.':'Cases not used to fit the model. They must also be relevant and free from leakage.',
'Still classification, but multi-class rather than binary. It is harder: with five classes there are far more ways to be wrong, and a single accuracy figure hides which ones you get wrong. Week 9.':'Still classification, but multiclass rather than binary. Difficulty depends on the data. Week 9 examines which categories are confused, beyond a single accuracy score.',
'If you cannot, you do not have a problem yet.':'A descriptive analysis question may not need a prediction target.',
'In Week 15, each student answers two unseen questions about the team’s work. The answers contribute to individual assessment.':'In Week 15, each student submits an individual written defence and reflection according to the published brief.'}
def main():
 plans=[]
 for path in sorted((ROOT/'IUEA_Teaching_Plan/decks').glob('*Week01*.pptx')):
  cohort=path.name[:7];original=OUT/'originals'/path.name;original.parent.mkdir(exist_ok=True)
  if not original.exists():original.write_bytes(path.read_bytes())
  slides=[];changes={}
  with zipfile.ZipFile(original) as z:
   for i in range(1,58):
    part=f'ppt/slides/slide{i}.xml';root=E.fromstring(z.read(part));edits=[]
    for paragraph in root.iter(A+'p'):
     runs=list(paragraph.iter(A+'t'));before=''.join(x.text or '' for x in runs);after=before
     for a,b in REPLACE.items():after=after.replace(a,b)
     if i==56:
      after=after.replace('Twelve this semester, best ten count. No resits.','Quiz category: 10%. Best nine of eleven count; Quiz 6 is waived.' if cohort in ('CML3111','CML3112','CML3113') else 'Quiz category: 10%. Best ten of twelve count.')
      if cohort in ('CML3112','CML3113'):after=after.replace('One per cent each. Tap View score and read the feedback.','Tap View score and read the feedback after submitting.')
     if before!=after:
      if runs:runs[0].text=after
      for x in runs[1:]:x.text=''
      edits.append({'before':before,'after':after})
    if edits:changes[part]=E.tostring(root,encoding='utf-8',xml_declaration=True).decode()
    slides.append(dict(number=i,notes=NOTES[i]))
  plans.append(dict(filename=path.name,slides=slides,replacements=changes))
 (OUT/'week1-review-plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2))
 print('Prepared notes for 171 Week 1 slides and targeted corrections.')
if __name__=='__main__':main()
