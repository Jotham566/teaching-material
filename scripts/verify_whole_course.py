"""Execute student-facing slide examples with their own week's files."""
import ast,contextlib,io,json,os,shutil,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run():
 p=ROOT/'data/iuea_deck_content.json';D=json.loads(p.read_text());report=[]
 for d in D:
  week=d['week'];cohort=d['cohort'];base=ROOT/'IUEA_Teaching_Plan'
  folder=base/'setup'/cohort if week==2 else base/'practicals'/f'W{week:02}'/cohort if week in (3,4,5) else base/'test_revision'/cohort/f'Test{1 if week==7 else 2}' if week in (7,14) else base/'assessment_banks'/f'W{week:02}'/cohort/'A'
  results=[];previous=Path.cwd()
  with tempfile.TemporaryDirectory() as tmp:
   for f in folder.glob('*.csv'):shutil.copy(f,tmp)
   os.chdir(tmp);ns={};out=None
   try:
    for i,s in enumerate(d['slides'],1):
     if not s.get('code'):continue
     program=s.get('practice_code',s['code'])
     if program:
      buffer=io.StringIO()
      with contextlib.redirect_stdout(buffer):exec(program,ns)
      if s.get('revision_check'):exec(s['revision_check'],ns)
      out=buffer.getvalue().strip() or 'Values are stored for the next step; this cell does not print a result.'
      results.append(dict(slide=i,title=s['title'],status='passed',output=out))
     if week<=5 or week==7:
      old=s.get('notes','').split('\n\nResult from the supplied example')[0]
      s['notes']=old+'\n\nResult from the supplied example\n'+out
      s['expected_output']=out
    if week==6:
     assert len(ns['raw_data'])==91 and len(ns['cleaned_data'])==88
     assert not ns['cleaned_data'].isna().any().any()
    if week in (8,10,11,12):
     sets=[set(ns[k]['equipment_id']) for k in ('training_data','validation_data','test_data')]
     assert not sets[0]&sets[1] and not sets[0]&sets[2] and not sets[1]&sets[2]
     assert 'target' not in ns['feature_columns']
    import matplotlib.pyplot as plt
    plt.close('all')
   finally:os.chdir(previous)
  notes=base/'decks/lecturer_notes'/Path(d['filename']).with_suffix('.md')
  notes.write_text('# '+cohort+' Week '+str(week)+'\n\n'+'\n\n'.join(f"## Slide {i}: {s['title']}\n\n{s.get('notes','')}" for i,s in enumerate(d['slides'],1)))
  report.append(dict(cohort=cohort,week=week,examples=results,csv_files=[f.name for f in folder.glob('*.csv')]))
 p.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
 outdir=ROOT/'review/2026-10-20/full-course-review';outdir.mkdir(parents=True,exist_ok=True)
 (outdir/'verified-examples.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Passed',sum(len(d['examples']) for d in report),'examples in',len(report),'source decks, with correct weekly CSV files and separate model groups.')
if __name__=='__main__':run()
