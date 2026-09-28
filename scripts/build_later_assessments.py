"""Create reviewable later-assessment banks and criterion-preserving hybrid maps."""
import json,csv,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';G=BASE/'grader'
sys.path.insert(0,str(G))
from engineering_contracts import DOMAINS,TASKS,dataset
from later_reasoning import ATOMS,SCENARIOS,cases,W08_CHOICE
# (task, marks, published criterion). Remaining marks stay in its original rubric criterion.
MAP={
 'W06':[('clean',5,'c1'),('summary',5,'c2'),('audit',2,'c2')],
 'W08':[('regression',7,'c1'),('errors',3,'c1')],
 'W09':[('classification',9,'c1')],
 'W10':[('split',6,'c1'),('regression',4,'c3')],
 'W11':[('features',5,'c1'),('ablation',5,'c2')],
 'W12':[('selection',5,'c1'),('errors',3,'c2')],
 'TEST1':[('summary',10,'c1'),('clean',10,'c2'),('charts',12,'c3'),('findings',20,'c4')],
 'TEST2':[('split',10,'c2'),('regression',10,'c3'),('errors',10,'c4')],
 'DA_PROJECT':[('clean',10,'c2'),('summary',10,'c3'),('charts4',12,'c3'),('findings',10,'c4')],
 'ML_PROJECT':[('regression',10,'c3'),('split',5,'c5'),('errors',5,'c5')],
}
OUT=BASE/'assessment_banks';OUT.mkdir(exist_ok=True)
HYBRID=G/'rubrics/hybrid';HYBRID.mkdir(exist_ok=True)
manifest={}
for aid,parts in MAP.items():
 original=json.loads((G/'rubrics'/f'{aid}.json').read_text());rubric=json.loads(json.dumps(original))
 rubric['id']=aid+'-2026.09-hybrid-r1';rubric['assessment_maximum']=original['maximum'];rubric['deterministic_maximum']=sum(x[1] for x in parts)
 for task,marks,cid in parts:
  next(c for c in rubric['criteria'] if c['id']==cid)['maximum']-=marks
 rubric['criteria']=[c for c in rubric['criteria'] if c['maximum']>0];rubric['maximum']=sum(c['maximum'] for c in rubric['criteria'])
 for c in rubric['criteria']:
  c['description']+=' Assess the written justification and interpretation for this criterion. Numerical checks are scored separately. Do not infer correct code execution from prose. Unverifiable visual, repository-history or model-fitting claims must be flagged as concerns, not awarded as established facts.'
 if aid=='W06':
  rubric['id']='W06-2026.09-hybrid-r7'
  atoms=[
   ('duplicates','c1',1,'Explicitly explains that retaining one record per repeated record_id prevents a repeated upload from counting the same observation twice. Merely reporting that a duplicate was removed is not a justification.'),
   ('invalid','c1',1,'Justifies excluding a missing target or a physically invalid load rather than inventing or clipping an unsupported value.'),
   ('impute','c1',1,'Justifies median imputation of missing ambient temperature while retaining the original raw data.'),
   ('limitations','c3',2.5,'Identifies at least one meaningful limitation: synthetic data, small sample, repeated equipment observations or imputation uncertainty.'),
   ('use','c3',2.5,'Restricts use to teaching/practice, or explains that deployment requires representative measured data. Equivalent wording is valid.')]
  rubric['criteria']=[dict(id=i,parent_criterion=parent,title=i.replace('_',' ').title(),maximum=m,description='Score this independently. Award '+str(m)+' if the submission '+text[0].lower()+text[1:]+' Otherwise award zero. Cite one short exact sentence supporting this item.') for i,parent,m,text in atoms]
 if aid in ATOMS:
  rubric['id']=aid+('-2026.09-hybrid-r5' if aid=='W08' else '-2026.09-hybrid-r2')
  rubric['scenario']=SCENARIOS[aid]
  rubric['criteria']=[dict(id=i,parent_criterion=parent,title=i.replace('_',' ').title(),maximum=m,description=f'Award {m} if the response {description}. Otherwise award zero. Score this criterion independently using the supplied scenario and a short exact quotation.') for i,parent,m,description in ATOMS[aid]]
  if aid=='W08':
   rubric['evaluation_mode']='atomic'
   rubric['criteria'][0]['description']=W08_CHOICE
  (G/'calibration_cases'/f'{aid}.json').write_text(json.dumps(cases(aid),indent=2)+'\n')
 if aid=='W06' or aid in ATOMS:
  for c in rubric['criteria']:c['binary']=True
 if aid=='TEST2':rubric['execution_gates']={'c2':dict(field='q1_marks',equals=10,reason='Data-preparation credit requires the published leakage-safe split check to pass.')}
 (HYBRID/f'{aid}.json').write_text(json.dumps(rubric,indent=2)+'\n')
 questions={f'q{i}':dict(marks=m,visible=False,prompt=TASKS[t][0]+': '+TASKS[t][1],answer_vars=[TASKS[t][0].split('(')[0]]) for i,(t,m,c) in enumerate(parts,1)}
 (G/'specs'/f'spec_{aid}.py').write_text(f'ASSIGNMENT={aid!r}\nTITLE={original["title"]!r}\nDEFAULT_COHORT=""\nQUESTION_ORDER={list(questions)!r}\nQUESTIONS={questions!r}\n')
 checks=',\n'.join(repr(f'q{i}')+': {"check": lambda ns: check(ns,'+repr(t)+')}' for i,(t,m,c) in enumerate(parts,1))
 (G/'specs/hidden'/f'spec_{aid}_hidden.py').write_text('from engineering_contracts import check\nQUESTIONS={'+checks+'}\n')
 for code,(domain,unit,*_) in DOMAINS.items():
  for variant in ('A','B','C') if aid.startswith('TEST') else ('A',):
   folder=OUT/aid/code/variant;folder.mkdir(parents=True,exist_ok=True)
   rows=dataset(code,{'A':17,'B':29,'C':43}[variant],dirty=True)
   with (folder/'engineering_data.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
   if aid=='W09':
    with (folder/'classification_case.csv').open('w') as f:
     w=csv.writer(f);w.writerow(['actual','predicted']);w.writerows(zip([1,0,1,1,0,1],[1,0,0,1,1,1]))
   investigation={
    'W08':'Which model improves on the training-mean baseline on a fixed validation set? Express the error in target units. What limits this comparison?',
    'W09':'Use classification_case.csv. Positive means a synthetic warning condition. Compute the confusion matrix, precision, recall and cost. Explain the 5:1 missed-warning/false-alarm cost assumption and why accuracy alone is insufficient. These costs are teaching assumptions, not approved operating limits.',
    'W10':'Why must repeated equipment observations stay in one partition? Keep E6 untouched during model selection. What change in operating conditions would invalidate your recommendation?',
    'W11':'Compare base and interaction features on the same equipment-group split: E1–E4 train, E5 validate, E6 final test. Define feature units and availability. Does the measured ablation support retaining the interaction?',
    'W12':'Compare candidates under one validation protocol, meeting both error and latency limits. Explain the trade-off and distinguish a local prediction explanation from global feature importance.',
    'TEST2':'Frame the prediction decision, justify group separation and preprocessing, compare a baseline with two fitted models, report errors in target units and state deployment limitations.',
    'ML_PROJECT':'Frame an engineering prediction decision. Compare a baseline and two fitted models under a fixed protocol, document prediction-time features, quantify held-out errors and state conditions of use.'
   }.get(aid,'What is the cleaned mean target in its unit? Which equipment group has the highest mean, and what is the gap to the lowest? What load/target pattern is visible, and why does it not establish causation?')
   instructions=[f'# {code} {aid}: {original["title"]} — variant {variant}',f'Investigate {domain}. Target units: {unit}. These are synthetic teaching records, not measurements suitable for deployment. Each record is one operating observation; equipment_id repeats across observations.',
    'Use your Student Registration Number in STUDENT_ID, including slashes. In filenames only replace slashes with underscores. Set COHORT to '+code+'.',
    'Numeric fields are numbers (missing values become None); parse CSV blanks accordingly. The public function interfaces below let the isolated grader evaluate your implementation on unseen records. The unseen records use the same schema and published rules. Implement the functions in the submitted notebook; do not hardcode the supplied answers. The numerical component does not prove the quality of the full investigation.',
    f'Published total: {original["maximum"]} marks. Deterministic component: {rubric["deterministic_maximum"]}. Written/evidence component: {rubric["maximum"]}. Original criterion totals are preserved.',
    '## Engineering questions',investigation, '## Required interfaces']
   if aid in SCENARIOS:instructions+=['## Supplied reasoning scenario',SCENARIOS[aid],'Interpret these supplied values for the written marks; they are not claims about results you measured. Your implementation is checked independently.']
   cells=[dict(cell_type='markdown',metadata={},source=[instructions[0]]),dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=[f'STUDENT_ID="YOUR_REGISTRATION_NUMBER"\nCOHORT="{code}"\n'])]
   for task,m,cid in parts:
    text=f'{TASKS[task][0]} — {m} marks within {cid}. {TASKS[task][1]}'
    instructions.append('- '+text);cells += [dict(cell_type='markdown',metadata={},source=[text]),dict(cell_type='code',metadata={},execution_count=None,outputs=[],source=['# Implement the interface here.\n'])]
   instructions += ['## Full investigation and evidence','Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete every original rubric criterion below, not just the checked functions. Include profiling, justified cleaning, question-led charts and your engineering recommendation where required. Keep raw data. State units and distinguish correlation from causation. Charts must be actual labelled figures in the notebook, not claims that charts exist. Include concise captions and an accessible report.']
   if aid.startswith('W'):
    instructions[-1]='Write your own explanation in the markdown cell headed `## My written evidence`. Keep that heading. Task prompts and code comments are excluded from reasoning marks. Complete the required functions and interpret the supplied scenario where provided. Broader project exercises and extra charts are formative practice; they do not add marks to this weekly submission. State units and limitations.'
    instructions += ['## Written assessment criteria']
    for c in rubric['criteria']:instructions += [f'- {c["title"]} ({c["maximum"]:g} marks): {c["description"]}']
   else:
    for c in original['criteria']:instructions += [f'- {c["title"]} ({c["maximum"]} total): {c["description"]}']
   for parent,gate in rubric.get('execution_gates',{}).items():instructions += ['Execution requirement for '+parent+': '+gate['reason']+' If this check fails, written marks in that criterion are zero; other criteria remain independently scored.']
   if aid.startswith('TEST'):
    instructions += ['## Timing and Part B','15 minutes setup, 120 minutes practical, 25 minutes typed offline reasoning with code execution prohibited, 20 minutes collection. No internet, messaging or AI. Answer: Why your main cleaning/model choice? What can your chart/metric not establish? What evidence would change your recommendation? What further data is required? Invigilated offline collection is authoritative; Google upload is a later transport step and must not impose an internet requirement during the test.']
   instructions += ['## Submission','Submit the notebook and concise accessible evidence through the assignment form. Keep a downloaded copy. The calibration/release status must be checked by the lecturer before issuing this bank. Repository history and visual design are not yet verified by the current automated checks.']
   if aid.startswith('W'):instructions[-1]='Submit exactly one complete notebook through the cohort form. Keep a downloaded copy. The form link and Kampala deadline are in the student package and final teaching slide.'
   (folder/'TASKS.md').write_text('\n\n'.join(instructions)+'\n')
   cells.append(dict(cell_type='markdown',metadata={},source=['## My written evidence\n\n']))
   (folder/f'{aid}_student.ipynb').write_text(json.dumps(dict(nbformat=4,nbformat_minor=5,metadata={},cells=cells),indent=2))
 manifest[aid]=dict(maximum=original['maximum'],deterministic_maximum=rubric['deterministic_maximum'],reasoning_maximum=rubric['maximum'],criterion_allocation=[dict(task=t,marks=m,criterion=c) for t,m,c in parts],release_status='DRAFT: validate reference solutions, equivalent variants and rubric calibration before issue')
(OUT/'assessment_components.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Built',len(MAP),'assessment contracts and 42 cohort/variant task banks; DRAFT pending validation')
