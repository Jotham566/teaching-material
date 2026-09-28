"""Prepare editable PowerPoint content and assessment mapping from issued sources.
No HTML is used by the teaching or packaging route.
"""
from pathlib import Path
import ast, json, re, hashlib, shutil
from datetime import datetime, timedelta, timezone
from beginner_pathway import WEEKS, COHORTS, VIDEOS
from beginner_quiz_bridges import BRIDGES
from beginner_visual_curriculum import enrich
from beginner_experiential import transform
from beginner_sequence import sequence, AUDIT
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/'IUEA_Teaching_Plan'; REVIEW=ROOT/'review/2026-09-15/ppt-revision'
REVIEW.mkdir(parents=True,exist_ok=True)
from beginner_practice_examples import EXTRAS as extras
LINKS=json.loads((ROOT/'data/submission_links.json').read_text()); QUIZZES=json.loads((ROOT/'data/quiz_links.json').read_text())
REG=json.loads((ROOT/'data/assessments.json').read_text())
SUFFIX={'CML3111':'Engineering','CML3112':'Design_Infrastructure','CML3113':'Mining_Petroleum'}
SOURCES=['https://docs.python.org/3/tutorial/introduction.html','https://docs.python.org/3/tutorial/controlflow.html','https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html','https://scikit-learn.org/stable/common_pitfalls.html']
SLOTS={'CML3111':'Friday 11:00–14:00, Room 115','CML3112':'Tuesday 11:00–14:00, Room 106','CML3113':'Friday 08:00–11:00, Room 105'}
SPECIAL={
2:[('The files in your ZIP',['proof_of_life.ipynb is the main class notebook.','01–04 are repair exercises we work through together.','hello_engineering.py shows the same idea as a script.','Return to proof_of_life.ipynb to finish the assignment.']),('A script and a notebook',['A .py script stores Python instructions in a text file.','A notebook stores code cells, explanations and saved outputs.','We use the notebook in Colab for this class.','The script is an optional comparison, not an extra upload.']),('The four repair exercises',['01: identify the deliberately unavailable module.','02: compare the required and actual Python versions.','03: locate the CSV and correct its file path.','04: restart and run in order to expose missing setup.'])],
3:[('Reading Python symbols',['= assigns a value to a name. == compares two values.','* multiplies. / divides. ** raises to a power.','Parentheses pass inputs when we call a function.','Indented lines belong to the block above them.']),('A function definition and a call',['def gives a reusable calculation a name and inputs.','Defining a function remembers the instructions.','Calling the function runs those instructions with values.','return sends the result back to the caller.'])],
4:[('One record at a time',['A CSV is a text table with a header row.','DictReader uses that header for dictionary keys.','CSV cells begin as text, even when they look numeric.','float("2.5") converts text into the number 2.5.'])],
5:[('Rows columns and units',['A row describes one observation. A column describes one field.','A DataFrame is pandas’ labelled table.','A Series is one labelled column.','kWh measures energy. kW measures power.'])],
6:[('An unusual value needs a reason',['A missing reading has no recorded value.','Zero is a recorded value and may be physically meaningful.','A large or negative value needs instrument and unit context.','Preserve the raw data and record every cleaning decision.'])],
8:[('A numerical prediction',['Regression predicts a number, such as cooling load in kW.','A feature is information available when predicting.','The target is the measured answer used during training.','Classification, next week, predicts a category.'])],
9:[('The positive class',['In this example, 1 means a warning is needed.','0 means a warning is not needed.','Actual is the reference label. Predicted is the model’s label.','A false negative misses a real warning.']),('Precision and recall',['Precision asks: of the warnings raised, how many were correct?','Recall asks: of the real warnings, how many did we detect?','A zero denominator needs an explicit rule.','Use the rule in your task brief when implementing the function.'])],
10:[('Training validation and final test',['Training data fit the model and preprocessing.','Validation data guide feature and model choices.','The final test evaluates choices after they are fixed.','A fresh test is needed if its answers influenced further choices.'])],
11:[('A feature has a meaning',['A feature is an input available at prediction time.','An interaction multiplies two inputs to express a joint pattern.','A better validation score can still reflect leakage.','Compare the same observations and explain the physical meaning.'])],
12:[('Error and practical constraints',['A smaller error can require more computation.','A candidate must meet every stated requirement.','Compare eligible models on the same validation observations.','Follow the published tie-break rule when scores tie.'])],
13:[('A useful README',['State the engineering question and target unit.','List the supplied data and required software versions.','Give the order for running the notebook from a fresh session.','State limitations and each member’s contribution.'])]}
TABLES={
4:('Tracing the loop',[['Step','reading','total after addition'],['Before loop','—','0'],['First','2','2'],['Second','4','6'],['Third','6','12']], 'There are three readings. The mean is 12 / 3 = 4. Reset total before repeating the calculation.'),
5:('Our small energy table',[['building','kwh'],['A','2'],['A','4'],['B','5'],['B','7']], 'The four observations total 18 kWh. Their mean is 4.5 kWh. Building totals are A: 6 and B: 12.'),
8:('Training observations',[['Input','Measured target'],['1','12'],['2','14'],['3','16'],['4','18']], 'Invented numbers for learning. The fitted line predicts 15 at input 2.5. The training mean is also 15 at this one example, so it cannot establish superiority.'),
9:('The four kinds of result',[['Actual / Predicted','Warning 1','No warning 0'],['Warning 1','TP = 1','FN = 1'],['No warning 0','FP = 1','TN = 1']], 'Rows are actual and columns are predicted. Read each paired observation into exactly one cell. Precision = 1/2. Recall = 1/2. Cost = 5 × FN + FP = 6 under this invented cost rule.'),
10:('Keeping equipment groups together',[['Observation','Equipment','Partition'],['1','A','Training'],['2','A','Training'],['3','B','Validation']], 'This toy split explains group separation. It does not establish a representative evaluation with only two pieces of equipment.'),
12:('A constrained model choice',[['Candidate','Validation error','Time (ms)'],['simple','3','2'],['complex','1','20']], 'Invented requirements: error at most 3 and time at most 10 ms. Only simple is eligible. No result here is a measured engineering benchmark.')}

REPLACEMENTS={
'Introduce one reusable calculation using the example below.':'A function stores a reusable calculation.',
'Then teach an if/else guard with a separate small example.':'A guard checks an input before a calculation runs.',
'Teach read_csv, nunique, division of columns, > filtering, mean and groupby(...).sum().idxmax() before the six public tasks.':'The six tasks use read_csv, nunique, division of columns, a > filter, mean and grouped totals.',
'Explain how a rate differs from a total and how a mean of rates differs from a total-cost/total-energy ratio.':'A mean of individual rates gives each observation equal weight. Total cost divided by total energy weights by energy.',
'Model copying with dict(row) and list.append.':'dict(row) copies a record. append adds an item to a list.',
'Walk through the published cleaning order before students write clean_records, summarize_records and audit_cleaning.':'The task brief specifies the cleaning order and returned outputs.',
'Teach set membership for duplicate IDs and grouped accumulation.':'A set records IDs already seen. Group summaries collect readings with the same equipment ID.',
'Teach training-only median imputation, Pipeline, list-to-table conversion and dictionary return values before those interfaces.':'Fit missing-value replacement on training data. A Pipeline joins preprocessing to the model.',
'Introduce grouped partitions now, not first in Week 10.':'Keep observations from the same equipment in one partition.',
'The written comparison is a supplied scenario; do not pretend to have measured its numbers.':'The written comparison supplies scenario values. Distinguish them from your own measured results.',
'demonstrate one-hot indicators before a fitting example':'use numeric indicator columns for categories',
'Demonstrate dictionary field access and ordered comparisons before asking learners to implement selection.':'Dictionary keys name the fields used to compare candidates.',
'Demonstrate a clean run from a fresh session with the actual files.':'A clean run starts in a fresh session with the actual files.',
'Demonstrate one unrelated practice table, one function check and saving a notebook plus the typed Part B document.':'Before test day, practise reading a small table, checking a function and saving the notebook and typed Part B evidence.',
'Use a blank practice packet, never a live test variant.':'Use the practice packet for rehearsal.',
'Release depends on the separate assessment-readiness checks; this practice material does not authorize release.':'Your lecturer will issue the test packet and collection instructions.',
'Keep its 145-minute assessment allocation and collection procedure.':'The assessed period has 120 practical minutes and 25 typed reasoning minutes.'
}
def student_text(t):
 for a,b in REPLACEMENTS.items():t=t.replace(a,b)
 return t

def sentences(t):return [part.strip() for part in re.split(r'\n\s*\n|(?<=[.!?])\s+(?=[A-Z0-9])',t) if part.strip()]
def stamp(t):return datetime.fromisoformat(t.replace('Z','+00:00')).astimezone(timezone(timedelta(hours=3))).strftime('%d %b %Y, %H:%M Kampala')
def pack_path(code,w):return BASE/'student_packages'/f'{code}_W{w:02}_student.zip'
def make_deck(code,w):
 c=COHORTS[code]; x=WEEKS[w]; slides=[]
 def add(title,body='',**kw):
  if isinstance(body,list):body='\n\n'.join(body)
  slides.append(dict(title=title,body=body,**kw))
 def prose(title,text,notes=''):
  # Simplify the complete passage before pagination so a cross-cohort sentence
  # cannot survive because its replacement spans two slide groups.
  original=text
  text=student_text(text)
  if w==3:
   text=re.sub(r'For the cohort task:.*?The brief determines which formula you implement\.', 'Use the formula for your programme shown earlier.', text, flags=re.S)
  parts=sentences(text);groups=[];current=[]
  for p in parts:
   if current and (len(current)>=4 or len(' '.join(current+[p]))>380):groups.append(current);current=[]
   current.append(p)
  if current:groups.append(current)
  for i,g in enumerate(groups): add(title if i==0 else title+' continued',g,notes=notes or original)
 def codeblock(title,program,explain):
  lines=program.splitlines();chunks=[lines[i:i+9] for i in range(0,len(lines),9)]
  for i,chunk in enumerate(chunks):
   add(title if len(chunks)==1 else f'{title} ({i+1}/{len(chunks)})',kind='code',code='\n'.join(chunk),practice_code=program if i==0 else '',notes=explain+'\n\nComplete practice code:\n'+program,caption='Read the code together. Predict the result before running.' if i==0 else 'Continue the same code cell, preserving indentation.')
 dt=datetime(2026,9,8 if code=='CML3112' else 11)+timedelta(weeks=w-1)
 add(x['title'],c['programmes'],kind='cover',subtitle=f'{code}   Week {w}\n{dt:%A %d %B %Y}\n{SLOTS[code]}',notes='Use PowerPoint Presenter View for these notes. Teach one example, pause for every learner to predict, then work an analogous example together. The practice notebook is a learning aid, not an extra graded upload. '+('These are preparation slides. Complete rehearsal before the official examination period.' if w in (7,14) else ''))
 add('Today’s learning',x['core'],notes='Ask learners to explain this goal in ordinary language. The first successful attempt matters more than covering optional extensions. Defer: '+x['stretch'])
 add('Recall and a first attempt',x['recall'],notes='Allow two minutes for everyone to try. Ask pairs to compare. If many cannot begin, show the first step and repeat with changed values. Checkpoint for today: '+x['gate'])
 if w not in (7,14,15):
  prose('The engineering context',c['context'])
  if w in (2,4):add('Your cohort data',[c['file'],'The column we will inspect: '+c['field'],'Keep the data file beside the notebook or upload it into the current Colab runtime.'])
  for title,body in SPECIAL.get(w,[]):add(title,body,notes='Demonstrate the terms on screen, then ask one learner to explain each term using the physical example. '+('Use the private Week2_Repair_Walkthrough.md for exact cohort repairs. Do not turn the four repairs into extra submissions.' if w==2 else ''))
  for i in range(0,len(x['terms']),2):
   terms=x['terms'][i:i+2]; prose(' and '.join(a for a,b in terms), '\n\n'.join(a+': '+b for a,b in terms))
  if w==3:
   prose('A calculation for your programme',c['formula']);codeblock('The calculation in Python',c['code'],'Read each name and unit. = assigns the number, * multiplies and / divides. print displays the result. '+c['formula'])
   add('A change to predict',c['change'],notes='Expected practice answer: '+c['answer']);add('The practice result',c['answer'])
  if w==3:
   add('Quantities and units',['Weight = mass × gravitational acceleration. Use g = 9.81 m/s² in the task.','Signed percentage error = 100 × (measured − expected) / expected, for a nonzero expected value.','Efficiency (%) = 100 × output power / input power.','The assignment returns None when input power is zero or negative.'])
   formulas={'CML3112':'Slab mass = area × thickness × density. Use metres and 2400 kg/m³ as specified.','CML3113':'Hydrostatic pressure (kPa) = density (kg/m³) × 9.81 (m/s²) × depth (m) / 1000. This is the pressure contribution of the fluid column.','CML3111':'Resistive power loss (W) = current (A) squared × resistance (ohms). In Python, current ** 2 means current multiplied by itself.'}
   add('Your programme formula',formulas[code])
  for i,e in enumerate(x['explain']):prose(['Understanding the example','Reading the instructions','Checking our reasoning','What happens next'][min(i,3)],e)
  if w in TABLES:
   title,table,note=TABLES[w];add(title,kind='table',table=table,notes=note,caption=note.split('. ')[0]+'.')
  if x['code']:
   for i,part in enumerate(x['code'].split('\n\n')):codeblock('Worked example' if i==0 else 'Worked example continued',part,' '.join(x['explain']))
   add('Expected output',x['out'],kind='output',notes='Compare the actual output character by character with this practice result. If it differs, read the first error and check the input, units, names and execution order. Do not copy this practice output into a graded answer.')
  for title,explanation,program in extras.get(w,[]):
   prose(title,explanation);codeblock(title+' in Python',program,explanation)
  add('Your turn',x['try_it'],notes='Give silent thinking time, then let pairs discuss. Rotate who types. This is practice, not a graded quiz. Expected response: '+x['answer'])
  add('Practice discussion',x['answer'],notes='Ask how the result was obtained. Reteach the smallest missing step instead of giving a longer lecture.')
  if x['video']:
   v=VIDEOS[x['video']];add('Short explainer and discussion',[v['author']+'\n'+v['title'],v['clip'],'Listening question: '+v['focus']],kind='link',url=v['url'],label='Open explainer video',notes=v['status']+'\nAfter viewing: '+v['after']+'\nPreview before class and stop after the selected short excerpt. If playback fails, teach the worked example. Video is optional. Source: '+v['url'])
   add('After the video',v['after'])
  prose('Preparing for the assignment',x['bridge'])
  if w in BRIDGES:prose(BRIDGES[w][0],BRIDGES[w][1],notes='Teach these concepts before the weekly quiz. Use changed numbers for practice. This slide supplies concepts, not the quiz key.')
  if w==5 and code!='CML3112':add('Week 5 support',['Friday 9 October has no normal class.','The lecturer will announce a supported replacement session or recording with a clinic.','Week 6 starts with 30 minutes of consolidation.'],notes='Confirm the actual Faculty-approved make-up or clinic arrangement. Do not assume a time or make video-only homework the replacement.')
 else:
  for e in x['explain']:prose('Preparation and expectations',e)
  if w in (7,14):
   codeblock('Practice before test day',x['code'],'Use this rehearsal before the assessment begins. Expected: '+x['out'])
   add('Test session',[ '00–15 minutes: briefing and file check.','15–135 minutes: individual practical work.','135–160 minutes: typed offline reasoning, with code execution prohibited.','160–180 minutes: save and hand in through invigilated offline collection.'],notes='Rehearsal and teaching examples happen before this timetable. Check the released packet, lab environment and assessment calibration status beforehand. Do not silently shorten the exam or release an unvalidated bank.')
  prose('Preparation checkpoint',x['gate']);prose('Your evidence',x['bridge'])
 # Public assignment contracts, never private grading keys.
 weekly=[a for a in REG if a['cohort']==code and a['track']=='IUEA' and a['week']==w]
 for a in weekly:
  aid=a['id'];task=BASE/'assessment_banks'/aid/code/'A/TASKS.md'
  if aid.startswith('W'):
   if w==2:
    add('Week 2 assignment',['Complete proof_of_life.ipynb and write your own README.md.','The README states your programme, file list and run instructions.','Include the repository URL in the form.','Upload the renamed notebook and README, not the ZIP or 01–04 repair notebooks.'],notes=(BASE/'setup/A2_assignment_brief.md').read_text())
   elif task.exists():
    text=task.read_text();domain=text.split('\n\n')[1]
    if w==9:domain=text.split('## Engineering questions')[1].split('## Required interfaces')[0].strip()
    prose('Your issued task',domain)
    interfaces=text.split('## Full investigation')[0]
    for item in re.findall(r'^- (.+)$',interfaces,re.M):
     signature,_,desc=item.partition(' — ');prose(signature, re.sub(r'^\d+ marks within c\d+\. ','',desc),notes='Public task contract. Explain input and output types before independent work. Source: '+str(task.relative_to(ROOT)))
    add('Written evidence',['Use the cell headed “My written evidence”.','Explain the supplied scenario in your own words.','State target units, reasons and limitations.','Submit one complete notebook containing code and written evidence.'],notes='Published criterion weights and exact requirements remain in TASKS.md. Broader project exercises are formative and do not add weekly marks. Local automated reasoning assessment remains subject to its release checks.')
   else:
    nb=next((BASE/'practicals'/f'W{w:02}'/code).glob('*.ipynb'));n=json.loads(nb.read_text());prompts='\n'.join(''.join(z['source']) for z in n['cells'] if z['cell_type']=='markdown')
    add('Your issued assignment',[f'Open {nb.name}.','Read every task and its input units before coding.','Keep the required function names and returned outputs.','Run the supplied visible checks, then restart and run all.'],notes=prompts)
    # Surface actual task headings in the deck.
    for cell in n['cells']:
     raw=''.join(cell['source'])
     if cell['cell_type']=='markdown' and raw.startswith('## '):
      title,_,body=raw.partition('\n');prose(title.lstrip('# '),body,notes=prompts)
    if w==4:prose('Week 4 rules',(nb.parent/'README.md').read_text().split('\n\n',1)[1])
  else:
   if task.exists():
    text=task.read_text();section=text.split('## Full investigation and evidence')[-1].split('## Submission')[0]
    prose(a['title'],section,notes=text)
   else:
    rubric=json.loads((BASE/'grader/rubrics'/f'{aid}.json').read_text())
    for criterion in rubric['criteria']:
     prose(criterion['title']+f" ({criterion['maximum']:g} marks)",criterion['description'],notes='Published '+aid+' criterion. Check the assessment grading-release status before issuing. Live questioning is formative. Source: '+str(BASE/'grader/rubrics'/f'{aid}.json'))
  entry=LINKS.get(a['key']);
  if entry:
   add(a['title']+' submission',[f'Opens: {stamp(entry["openAt"])}',f'Deadline: {stamp(entry["closeAt"])}','Use your full Student Registration Number in the form.','Keep the submitted files and confirmation.'],kind='link',url=entry['url'],label='Open '+aid+' assignment form',notes='The form link is cohort-specific. Recheck the live form and release status before class. These scheduled assignment dates are separate from the quiz activation window. The issued brief defines the required files, even if the form accepts additional formats. Source: data/submission_links.json')
 # Project milestones must be taught before the deadline, not first on submission day.
 if w in (5,6,11,12,13):
  aid='DA_PROJECT' if w in (5,6) else 'ML_PROJECT';entry=LINKS[code+'|'+aid]
  add('Project preparation',['Use the published '+('data analysis' if aid=='DA_PROJECT' else 'machine learning')+' project brief.','Build the evidence gradually in your project notebook.','Keep raw data, labelled charts, run instructions and individual contributions.',f'Published deadline: {stamp(entry["closeAt"])}'],notes='Explain the released brief now. Confirm its grading-release checks before assigning it. Avoid treating weekly practice as a substitute for the project evidence. The project brief remains authoritative.')
 q=QUIZZES.get(f'{code}|{w}')
 if q:add('Week '+str(w)+' quiz',['Answer individually after the lecturer activates the quiz.','Available for 24 hours from activation.','Use your Student Registration Number and registered account.','The lecturer will confirm the exact closing time.'],kind='link',url=q,label='Open this week’s quiz',qr=f'qr/quiz_{code}_W{w:02}.png',notes='Activate the matching open_W'+str(w)+'_'+code+' function in Quiz Controls, then confirm the 24-hour close time. Opening this slide or clicking its link does not activate the form. The 24 hours is the availability window. Keep existing quiz scoring and form rules. Do not show private answer keys.')
 add('Before you leave',[x['gate'],'Save your work and check the required submission files.',x['next']],notes='Ask every learner for an individual response. Record one misconception to revisit at the start of the next class. If a deadline changed, announce the exact Kampala date and update the source registry before rebuilding slides.')
 for slide in slides:
  original=slide.get('body','')
  slide['notes']=slide.get('notes','')+'\n\nTeaching context: '+original+'\n\nReference sources: '+'\n'.join(SOURCES)
  slide['body']=re.sub(r'(?m)^[-#]+\s*', '', student_text(original))
  if w==3 and 'For the cohort task:' in slide['body']:
   slide['body']=re.sub(r'For the cohort task:.*?The brief determines which formula you implement\.', 'Use the formula for your programme shown earlier.', slide['body'], flags=re.S)
  if 'TEST' in slide.get('label',''):
   slide['body']='Offline invigilated collection is authoritative.\n\nGoogle upload is a later transport step.\n\nSave the notebook and the typed Part B evidence as instructed by the invigilator.\n\nNo internet, messaging or AI during the test.'
 enrich(slides,w)
 transform(slides,w,code)
 sequence(slides,w,code)
 filename=f'{code}_Week{w:02}_{SUFFIX[code]}.pptx'
 from reviewed_notes_overlay import apply_reviewed_notes
 apply_reviewed_notes(slides,filename)
 return dict(cohort=code,week=w,filename=filename,slides=slides,assessment_ids=[a['id'] for a in weekly],quiz_url=q)

from iuea_foundations_revision import revise
# Week 2 is already taught: preserve its published content during this revision.
existing=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
decks=[next(d for d in existing if d['cohort']==c and d['week']==w) if w==2 else revise(make_deck(c,w)) for c in COHORTS for w in WEEKS if not(c=='CML3112' and w==2)]
(ROOT/'data/iuea_deck_content.json').write_text(json.dumps(decks,indent=2)+'\n')
(REVIEW/'deck-content.json').write_text(json.dumps(decks,indent=2)+'\n')
print(f'Prepared {len(decks)} decks, {sum(len(d["slides"]) for d in decks)} slides')

(ROOT/'review/2026-09-16/sequential').mkdir(parents=True,exist_ok=True)
(ROOT/'review/2026-09-16/sequential/sequence-audit.json').write_text(json.dumps(AUDIT,indent=2)+'\n')
