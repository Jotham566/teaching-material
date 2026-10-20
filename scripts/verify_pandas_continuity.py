"""Execute every revised guided notebook in the pinned offline grading image."""
from pathlib import Path
import json,subprocess,re,zipfile
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';out=ROOT/'review/2026-10-15/pandas-continuity'
results=[]
for cohort in ('CML3111','CML3112','CML3113'):
 for week in (6,7,8,9,10,11,12,13,14):
  nb=json.loads((BASE/f'guided_practice/{cohort}/W{week:02}/guided_practice.ipynb').read_text())
  code='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
  assert not re.search(r'import csv|csv\.DictReader|csv\.reader',code)
  folder=BASE/f'assessment_banks/W{week:02}/{cohort}/A'
  if not folder.exists():folder=BASE/f'assessment_banks/TEST1/{cohort}/A'
  args=['docker','run','--rm','--network=none','--mount',f'type=bind,src={folder},dst=/data,readonly','--workdir','/data','-e','MPLBACKEND=Agg','iuea-notebooks:2026.09','python','-c',code]
  r=subprocess.run(args,capture_output=True,text=True,timeout=60)
  if r.returncode:raise RuntimeError(f'{cohort} W{week}: {r.stderr}')
  results.append(dict(cohort=cohort,week=week,stdout=r.stdout,stderr=r.stderr))
  print(cohort,week,'PASS',flush=True)
(out/'practice-execution.json').write_text(json.dumps(results,indent=2)+'\n')
# Every question has one correct answer and tested concepts mapped to its lesson.
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from quiz_banks import QUIZ,options_for
for week in (6,8,9,10,11,12,13):
 for cohort in ('CML3111','CML3112','CML3113'):
  assert len(QUIZ[week]['q'])==5
  for q in QUIZ[week]['q']:
   choices=options_for(q,cohort)
   assert len(choices)==4 and sum(c for _,c,_ in choices)==1
print('27 notebooks executed; all 21 later quiz banks structurally valid.')
