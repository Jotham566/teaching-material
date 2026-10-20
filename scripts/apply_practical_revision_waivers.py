"""Apply authorized 19 October cohort exceptions to teaching handouts."""
import json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan'
NOTICE='A6 and Quiz 6 are waived for this cohort. This is ungraded practical revision. No assignment upload or quiz response is required. Previous submissions remain on record but do not count towards coursework marks.'
p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text())
for d in decks:
 if d['cohort'] not in ('CML3112','CML3113') or d['week'] not in (6,7):continue
 code=d['cohort']
 if d['week']==6:
  d['assessment_ids']=[];d['quiz_url']=None
  replacements={
   'Your issued task':('Ungraded cleaning practice','Open guided_practice.ipynb and upload engineering_data.csv.\n\nRun the examples in slide order. Explain each result in your own words.\n\nA6 and Quiz 6 are waived. No upload is required.'),
   'Written evidence':('Explain your cleaning choices','In your practice notebook, write why you removed a duplicate and how you handled a missing value.\n\nUse the actual row counts and column names from your results.\n\nThis is practice, not a graded report.'),
   'Cleaning and quality submission':('Save your practice notebook','A6 is not assigned for this cohort.\n\nSave your work in Google Drive so you can revise it later.\n\nYou do not need to upload it to an assignment form.'),
   'Week 6 quiz':('Check your understanding','Quiz 6 is not assigned for this cohort.\n\nExplain: why is a missing value different from zero?\n\nExplain: why keep the original CSV unchanged?\n\nCompare your answers with the earlier examples.'),
   'Revision and submission checklist':('Practical revision checklist','Restart and run your practice notebook from the top.\n\nCheck the cleaning steps, summary values and chart labels.\n\nNext, work through the Test 1 revision PDF with its matching practice CSV. No practice upload is required.')}
  for s in d['slides']:
   if s['title'] in replacements:
    title,body=replacements[s['title']];s.clear();s.update(title=title,body=body,kind='steps',notes=NOTICE+'\nExplain the steps on this slide. A blank means unrecorded, whereas zero is a measured value. Keep the original file so the changes can be checked. Save practice in Drive; do not activate A6 or Quiz 6.')
   else:
    for field in ['body','notes']:
     if field in s:s[field]=s[field].replace('The assignment caller','The calling cell').replace('required by the assignment','specified in the example').replace('assessed function','practice function').replace('the learner’s own assessed answer','the learner’s own practice answer').replace('graded assignment','practice exercise').replace('required assignment','practice').replace('This is the actual graded task','This is an optional practice task')
  for slide in d['slides']:
   if slide['title']=='Pandas inside the required function':slide['title']='Pandas inside a function'
  d['slides'][0]['subtitle']=code+'   Week 6\nCleaning and practical revision\nA6 and Quiz 6: not assigned'
 else:
  d['slides'][0]['subtitle']=code+'   Week 7\nPractical revision before Test 1\nTest time: confirm with the lecturer'
  d['slides'][0]['notes']=NOTICE+'\n'+d['slides'][0]['notes'].replace(NOTICE+'\n','')
  # The test-day instructions remain intact, clearly separate from revision.
 if d['week']==6:
  cues={
   'Ungraded cleaning practice':'Open guided_practice.ipynb, then upload engineering_data.csv through Colab Files. Run the loading cell and confirm the expected column names. Learners follow this notebook during class; no separate A6 notebook is required.',
   'Explain your cleaning choices':'Ask learners to identify one duplicated record ID and one missing value in the displayed data. Their explanation should name the column, state the chosen action and distinguish a measured value from an estimate. This is a short revision note, not a submitted report.',
   'Save your practice notebook':'Use File > Save in Google Drive. Ask learners to check the notebook name in Drive and reopen it. A saved practice notebook is for their revision; the closed A6 form does not indicate unfinished work.',
   'Check your understanding':'Expected answers: a missing value means no observation was recorded; zero is an actual numeric value. Keeping the raw CSV lets us repeat the analysis and check what was changed. If a learner confuses blank and zero, compare an unrecorded temperature with a measured 0 degrees C.',
   'Practical revision checklist':'Restart the session and run from the first cell. If the CSV is missing, upload it again. Check that axes show the quantity and unit. Then switch to a NEW notebook and the cohort Test1_practice.csv for the Week 7 examples; do not mix its column names with the Week 6 file.'}
  for slide in d['slides']:
   if slide['title'] in cues:slide['notes']=cues[slide['title']]+'\n'+NOTICE
 for i,slide in enumerate(d['slides'],1):slide['sequence_number']=i
 d['practical_revision_waiver']='2026-10-19'
 notes=BASE/'decks/lecturer_notes'/Path(d['filename']).with_suffix('.md')
 notes.write_text('# '+code+' Week '+str(d['week'])+' lecturer notes\n\n'+NOTICE+'\n\n'+'\n\n'.join(f"## Slide {i}: {s['title']}\n\n{s.get('notes','')}" for i,s in enumerate(d['slides'],1)))
p.write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n')
for code in ('CML3112','CML3113'):
 guide=f'''# {code}: practical revision before Test 1

{NOTICE}

1. Bring your laptop and sign in to Google Colab.
2. Finish the Week 6 cleaning examples with guided_practice.ipynb and engineering_data.csv.
3. Open the Test 1 revision PDF and upload {code}_Test1_practice.csv to a new Colab notebook.
4. Run the worked examples in order. Try the practice questions before reading the answers.
5. Check missing values, duplicates, summaries, functions, charts and units. Explain your results.
6. Restart and run all cells. Save your notebook in Drive. There is nothing to submit for this revision session.

The actual test uses different files released through the timed test portal. Wait for the lecturer to announce its date and time. The test-day section of the Week 7 slides explains the real submission process; do not submit practice files there.

Coursework: best 9 of 11 assigned quizzes (10%); best 7 of 10 assigned weekly assignments (10%). A6 and Quiz 6 are excluded, including any previously recorded marks. Other assessments keep their weights.
'''
 (BASE/'student_guides'/code/'W06.md').write_text(guide)
 folder=BASE/'assessment_banks/W06'/code/'A'
 for name in ['ASSIGNMENT_INSTRUCTIONS.md','ASSIGNMENT_INSTRUCTIONS.txt']:(folder/name).write_text(guide)
 p=folder/'TASKS.md';s=p.read_text();s=s if s.startswith('# NOT ASSIGNED') else '# NOT ASSIGNED — optional practice only\n\n'+NOTICE+'\n\n'+s;p.write_text(s)
 p=folder/'W06_student.ipynb';nb=json.loads(p.read_text())
 if not nb['cells'][0].get('metadata',{}).get('waiver_notice'):nb['cells'].insert(0,{'cell_type':'markdown','metadata':{'waiver_notice':True},'source':['# Optional practice — no submission\n',NOTICE]})
 p.write_text(json.dumps(nb,ensure_ascii=False,indent=1)+'\n')
 # Simple practice-only handout avoids assignment instructions and grading helpers.
 out=BASE/'student_packages'/f'{code}_W06_student.zip'
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('00_START_HERE.txt',guide)
  z.write(BASE/'guided_practice'/code/'W06/guided_practice.ipynb','guided_practice.ipynb')
  z.write(folder/'engineering_data.csv','engineering_data.csv')
  z.write(BASE/'setup/STUDENT_HOW_TO.md','STUDENT_HOW_TO.md')
