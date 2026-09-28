"""Publish criterion rubrics for document-based work; preserve course weights."""
import json
from pathlib import Path
from assessment_registry import records
from plan_content import RUBRICS
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'IUEA_Teaching_Plan/grader/rubrics';OUT.mkdir(exist_ok=True)
DESCRIPTIONS={
 'W01': [('Problem framing',30,'Three specific engineering problems, each with a clear quantity/category and reason ML is or is not suitable.'),('Data and feasibility',40,'For each problem, plausible features, a target where appropriate, data source and a stated limitation.'),('Judgement',30,'A defensible choice of one dataset/problem and explanation of why the evidence could support the question.')],
 'W02': [('Execution order',50,'Explains that each increment uses the current readings value, so successive runs after initialization give 17, 22, 27; restarting clears state and Run All initializes before incrementing.'),('Repository evidence',50,'README supplies the program context, notebook and CSV file list, upload/run instructions and a meaningful save/version instruction.')],
 'W04': [('Results',50,'Reading report supplies correct, reproducible summaries with units and boundary rules.'),('Interpretation',30,'Explains one supported finding and its engineering relevance without claiming causation.'),('Reproducibility',20,'Input source and run instructions make the result reproducible.')],
 'W06': [('Cleaning decisions',40,'Defect register identifies actual defects and justified handling; preserves raw data.'),('Verification',35,'Before/after counts and checks reconcile with cleaning code and outputs.'),('Quality statement',25,'States remaining limitations and appropriate uses of the cleaned data.')],
 'W08': [('Evaluation',50,'Same held-out cases compare regression against a baseline, with error in physical units.'),('Decision',30,'Recommendation follows the evidence and acknowledges model limitations.'),('Reproducibility',20,'Data, split and run instructions are specified.')],
 'W09': [('Classification evidence',45,'Confusion counts and metrics are internally consistent.'),('Costs and choice',35,'Metric choice follows the stated relative costs of false positives/negatives.'),('Limits',20,'Appropriate deployment limitation and reproducible setup.')],
 'W10': [('Validation',50,'Split and preprocessing avoid identified leakage; test data are not used for fitting or model selection.'),('Conditions of use',30,'Names supported use conditions and plausible failure under distribution change.'),('Evidence',20,'Baseline and evaluation are reproducible and comparisons use the same cases.')],
 'W11': [('Features',35,'Feature dictionary defines inputs, units, transformations and availability at prediction time.'),('Ablation',45,'Same-split comparison measures the contribution of proposed features without leakage.'),('Decision',20,'Retain/drop decision follows observed evidence rather than assumed improvement.')],
 'W12': [('Recommendation',40,'Selects a model using the stated decision requirements rather than score alone.'),('Evidence',35,'Comparison uses consistent validation and distinguishes local explanation from global importance.'),('Limits',25,'States assumptions, failure conditions and what would change the recommendation.')],
 'DA_PROJECT': [('Question and data',20,'Clear engineering question, source/licence, units and credible data provenance.'),('Investigation',40,'Reproducible cleaning and question-driven charts support the findings.'),('Judgement',25,'Conclusions follow evidence and acknowledge limitations.'),('Communication',15,'Brief answers the question clearly and directs readers to supporting outputs.')],
 'ML_PROJECT': [('Problem and data',20,'Named target and features available at prediction time; legitimate data source.'),('Evaluation',35,'Baseline, leakage-safe pipeline and consistent validation support model comparison.'),('Reproducibility',25,'Restart-and-run-all workflow with data and dependency instructions.'),('Recommendation',20,'Decision, limitations and contribution evidence are explicit.')],
 'DEMO': [('Answer',35,'Presentation states the question and evidence-supported result clearly.'),('Evidence',35,'Slides/notes explain how results were obtained and key trade-offs.'),('Reflection',30,'Individual reflection identifies a specific contribution, limitation and response to a technical question.')],
 'S05': [('Rep/month grain',25,'Correct delivered-order rep/month keys with no duplicates; extra or missing rows reduce credit.'),('Gross amount',25,'Gross amounts match the executed reference within 1 UGX after rounding.'),('Returned amount',25,'Returned amounts match the executed reference within 1 UGX after rounding.'),('Net amount',25,'Net amounts match the executed reference within 1 UGX after rounding.')],
 'S09': [('Cleaning log',40,'Documents actual defects, handling and checks without destroying raw data.'),('Reconciliation',40,'Pandas results reconcile to SQL with an explicit rounding tolerance.'),('Reproducibility',20,'Runnable workflow produces the supplied output from raw inputs.')],
 'S13': [('Question',20,'Specific business question and appropriate population/period.'),('Analysis',40,'Correct grain, denominator, comparisons and reproducible evidence.'),('Judgement',25,'Finding and recommendation distinguish evidence from causation.'),('Communication',15,'Chart and narrative make the answer clear.')],
 'S15': [('Model and measures',35,'Relationships and delivered revenue/AOV use consistent populations; totals reconcile.'),('Dashboard',25,'Purposeful visuals and filters communicate the main finding.'),('Recommendation',25,'Decision includes evidence, conditions and a meaningful limitation.'),('Presentation',15,'Slides and narration notes answer the question before methods.')],
 'TEST1': [('Correctness',65,'Submitted code and outputs correctly answer the issued test tasks.'),('Interpretation',20,'Answers interpret outputs with units and justified conclusions.'),('Reproducibility',15,'Notebook runs from the provided inputs in the declared environment.')],
 'TEST2': [('Correctness',55,'Submitted pipeline answers the issued test tasks with consistent metrics.'),('Validation',30,'No test leakage and a defensible baseline/comparison.'),('Interpretation',15,'Recommendation follows results and states limitations.')]
}
# Preserve published Faculty course criteria and weights; do not invent a second scheme.
for assessment,published in {
 'ML_PROJECT':'Engineering ML Project (25%) - as specified by the lecturer',
 'DA_PROJECT':'Data Analysis Project (10%)',
 'TEST1':'Practical Test 1 - Data Investigation (15%)',
 'TEST2':'Practical Test 2 - End-to-End Engineering ML (20%)',
 'DEMO':'Demo, viva & individual reflection (10%)',
}.items():
 DESCRIPTIONS[assessment]=RUBRICS[published]

W02_RUBRIC = {'id': 'W02-2026.09-r3', 'title': 'Proof of life', 'maximum': 6, 'criteria': [{'id': 'state', 'title': 'Current value', 'maximum': 1, 'description': 'Award 1 if the student explains that each execution adds five to the value left by the previous execution (or accurately gives 17, 22, 27 after initialization at 12). Equivalent wording is valid. Otherwise 0.'}, {'id': 'restart', 'title': 'Restart', 'maximum': 1, 'description': 'Award 1 if the student explains that restarting clears stored variable/kernel state. Equivalent wording is valid. Otherwise 0.'}, {'id': 'run_all', 'title': 'Run All', 'maximum': 1, 'description': 'Award 1 if the student explains that running all cells from the top initializes 12 before adding five and yields 17. Equivalent wording is valid. Otherwise 0.'}, {'id': 'files', 'title': 'Repository context and files', 'maximum': 1, 'description': 'Award 1 if the README identifies the engineering/program context and names the notebook and CSV. Otherwise 0.'}, {'id': 'run', 'title': 'Run instructions', 'maximum': 1, 'description': 'Award 1 if the README describes uploading/opening required files and executing the notebook from the top or using Restart and Run All. Otherwise 0.'}, {'id': 'save', 'title': 'Save and version', 'maximum': 1, 'description': 'Award 1 if the README gives a meaningful instruction to save/download the notebook or stage and commit changed files. Otherwise 0.'}]}
for criterion in W02_RUBRIC['criteria']:criterion['binary']=True
for a in records():
 if a['id'] not in DESCRIPTIONS:continue
 maximum=6 if a['id']=='W02' else a['maximum']
 criteria=[dict(id=f'c{i}',title=t,maximum=maximum*weight/100,description=d) for i,(t,weight,d) in enumerate(DESCRIPTIONS[a['id']],1)]
 rubric=dict(id=a['id']+'-2026.09',title=a['title'],maximum=maximum,criteria=criteria)
 if a['id']=='W02':rubric=W02_RUBRIC
 (OUT/(a['id']+'.json')).write_text(json.dumps(rubric,indent=2)+'\n')
