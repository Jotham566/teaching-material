"""Execute worked examples against the supplied local data; audit advertised scope."""
from schools_camp_content import ROOT,ML,DA,ROADMAP
import contextlib,io,json,os,shutil,sqlite3,tempfile,traceback,zipfile
from pathlib import Path
os.environ['MPLBACKEND']='Agg'
import matplotlib.pyplot as plt
import nbformat
results=[]
for code,lessons in [('ML',ML),('DA',DA)]:
 assert len(lessons)==24
 for i,l in enumerate(lessons,1):
  ident=f'{code}{i:02}';sheet=ROOT/'student_materials'/code/f'{ident}.md'
  assert sheet.exists() and all(l[k] for k in ['title','explain','demo','expected','task','answer','repair'])
  assert (ROOT/'instructor_materials'/code/f'{ident}_guide.md').exists()
  row={'session':ident,'mode':l['mode'],'status':'structured lesson checked'}
  if code in ('ML','DA'):nbformat.validate(nbformat.read(ROOT/'student_materials'/code/f'{ident}.ipynb',as_version=4))
  if l['mode']=='python':
   with tempfile.TemporaryDirectory() as tmp:
    for f in (ROOT/'data').glob('*.csv'):shutil.copy2(f,tmp)
    previous=os.getcwd();os.chdir(tmp);output=io.StringIO()
    try:
     with contextlib.redirect_stdout(output):exec(l['demo'],{'__name__':'__main__'})
     row.update(status='worked Python executed',output=output.getvalue().strip());plt.close('all')
    finally:os.chdir(previous)
  elif l['mode']=='sql':
   db=sqlite3.connect(ROOT/'data'/'camp_shop.sqlite')
   for part in l['demo'].split(';'):
    if part.strip():db.execute(part).fetchall()
   row['status']='worked SQL executed';db.close()
  results.append(row)
ref=json.loads((ROOT/'instructor_materials'/'reference_values.json').read_text())
db=sqlite3.connect(ROOT/'data'/'camp_shop.sqlite')
assert db.execute('SELECT COUNT(*),SUM(units),SUM(units*unit_price_ugx) FROM sales').fetchone()==(ref['row_count'],ref['total_units'],ref['revenue_ugx'])
assert db.execute('SELECT COUNT(*) FROM sales LEFT JOIN products USING(item)').fetchone()[0]==60
assert db.execute('SELECT COUNT(*) FROM sales WHERE units IS NULL').fetchone()[0]==0
assert len({x['title'] for x in ML})==24 and len({x['title'] for x in DA})==24
out=io.StringIO()
with contextlib.redirect_stdout(out):exec((ROOT/'instructor_materials'/'ml18_reference.py').read_text(),{'__name__':'__main__'})
report={'sessions':48,'notebooks_validated':48,'python_examples_executed':sum(x['mode']=='python' for x in results),'sql_examples_executed':sum(x['mode']=='sql' for x in results),'reference_values':ref,'ml18_reference_output':out.getvalue(),'results':results,'limits':'Python/Jupyter and DB Browser require device preflight; lesson comprehension requires a beginner pilot. No school submission platform deployed.'}
p=ROOT.parents[1]/'review/2026-09-26/schools-camp/verification.json';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['results','reference_values','ml18_reference_output']},indent=2))

# Additional foundation labs: validate notebook structure and exact worked outputs.
from build_schools_camp_foundations import LABS
expected = [[3000,1000,1000,3000,4000],[2,40,2,6],[4,4,2,2/6,100*2/6]]
lab_results=[]
for i,lab in enumerate(LABS,1):
 ident=f'F{i:02}'
 nb=nbformat.read(ROOT/f'student_materials/ML/{ident}.ipynb',as_version=4)
 nbformat.validate(nb)
 capture=io.StringIO()
 with contextlib.redirect_stdout(capture):exec(lab['code'],{})
 output=capture.getvalue().strip()
 if i<4:
  actual=[float(v) for v in output.splitlines()]
  assert len(actual)==len(expected[i-1])
  assert all(abs(a-b)<1e-8 for a,b in zip(actual,expected[i-1]))
 else:assert output.splitlines()==['2 2','2','260000','340000']
 assert (ROOT/f'instructor_materials/ML/{ident}_guide.md').exists()
 lab_results.append({'lab':ident,'after':lab['after'],'output':output,'status':'passed'})
report.update(foundation_labs=lab_results,notebooks_validated=52,python_examples_executed=sum(x['mode']=='python' for x in results)+4,meetings={'ML':28,'DA':24})
p.write_text(json.dumps(report,indent=2)+'\n')
print('Four foundation labs passed; 52 notebooks validated; Python and SQL examples executed.')
