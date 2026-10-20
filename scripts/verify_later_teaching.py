"""Execute each complete slide example using its issued CSV and refresh lecturer results."""
import ast,contextlib,io,json,os,shutil,tempfile,re
from pathlib import Path
from descriptive_teaching_names import MEANINGS,explain_statement,name_map,rename_code
from test_revision_slides import revision_slides
ROOT=Path(__file__).resolve().parents[1]
MEANINGS.update(X_train='training input columns, excluding the target',y_train='observed training targets in matching row order',X_valid='validation input columns in training-column order',y_valid='observed validation targets, used only for evaluation',mae='mean absolute error in the target unit',rmse='root mean squared error in the target unit')
def run():
 (ROOT/'review/2026-10-20').mkdir(parents=True,exist_ok=True)
 p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text());report=[]
 for d in decks:
  if d['week']<8 and d['week']!=6:continue
  originals={s['title']:s.get('revision_check','') for s in revision_slides(d)} if d['week']==14 else {}
  with tempfile.TemporaryDirectory() as tmp:
   folder=ROOT/'IUEA_Teaching_Plan'/('test_revision/'+d['cohort']+'/Test2' if d['week']==14 else f"assessment_banks/W{d['week']:02}/{d['cohort']}/A")
   for csv in folder.glob('*.csv'):shutil.copy(csv,tmp)
   previous=Path.cwd();os.chdir(tmp);ns={};examples=0;notes='';check=''
   try:
    for s in d['slides']:
     if not s.get('code'):continue
     full=s.get('practice_code',s['code'])
     if full:
      output=io.StringIO()
      with contextlib.redirect_stdout(output):exec(full,ns)
      examples+=1
      notes=s.get('teaching_explanation','')+'\n\nStep-by-step explanation\n\n'+'\n\n'.join(ast.unparse(n)+'\n'+explain_statement(n) for n in ast.parse(full).body)
      notes+='\n\nVerified result with the supplied CSV\n'+(output.getvalue().strip() or 'This cell stores values for the next example; it does not print a result.')
      notes+='\n\nRun this complete example after the preceding examples. Continuation slides belong to the same notebook cell.'
      title=s.get('original_example_title',re.sub(r' \(\d+/\d+\)$','',s['title']))
      if d.get('stepwise_pipeline_revision') and not s.get('last_example_step'):title=''
      mapping=name_map(d['week']);mapping.update(mae='mae',rmse='rmse')
      check=rename_code(originals.get(title,''),mapping) if originals.get(title) else ''
      if check:exec(check,ns)
      s['revision_check']=check
     else:s['revision_check']=''
     s['notes']=notes
     s['expected_output']=notes.split('Verified result with the supplied CSV\n',1)[-1].split('\n\nRun this complete example')[0]
     if d['week']==14:s['revision_example']=True
    report.append({'cohort':d['cohort'],'week':d['week'],'complete_examples_passed':examples})
   finally:os.chdir(previous)
  note=ROOT/'IUEA_Teaching_Plan/decks/lecturer_notes'/Path(d['filename']).with_suffix('.md')
  note.write_text('# '+d['cohort']+' Week '+str(d['week'])+'\n\n'+'\n\n'.join(f"## Slide {i}: {s['title']}\n\n{s.get('notes','')}" for i,s in enumerate(d['slides'],1)))
 p.write_text(json.dumps(decks,ensure_ascii=False,indent=2)+'\n')
 (ROOT/'review/2026-10-20/later-teaching-execution.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Verified',sum(x['complete_examples_passed'] for x in report),'examples across',len(report),'decks')
if __name__=='__main__':run()
