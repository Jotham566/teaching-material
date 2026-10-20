"""Execute slide code against the supplied files and record each result."""
from pathlib import Path
import json,subprocess,re
ROOT=Path(__file__).resolve().parents[1]
runner='''import json,os,io,contextlib,traceback
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
decks=json.loads(Path("/repo/data/iuea_deck_content.json").read_text());results=[]
for d in decks:
 if not d.get("csv_examples_revision"):continue
 w=d["week"];c=d["cohort"]
 if w<=5:folder=Path(f"/repo/IUEA_Teaching_Plan/practicals/W{w:02}/{c}")
 else:
  source={7:6,14:12}.get(w,w)
  folder=Path(f"/repo/IUEA_Teaching_Plan/assessment_banks/W{source:02}/{c}/A")
 os.chdir(folder);env={}
 for s in d["slides"]:
  if s["kind"]!="code" or not s.get("practice_code"):continue
  stream=io.StringIO()
  with contextlib.redirect_stdout(stream):exec(s["practice_code"],env)
  results.append(dict(cohort=c,week=w,title=s["title"],code=s["practice_code"],output=stream.getvalue(),file=str(folder)))
  plt.close("all")
print(json.dumps(results))
'''
r=subprocess.run(['docker','run','--rm','--network=none','--mount',f'type=bind,src={ROOT},dst=/repo,readonly','iuea-notebooks:2026.09','python','-c',runner],capture_output=True,text=True,timeout=240)
if r.returncode:raise RuntimeError(r.stderr)
results=json.loads(r.stdout);out=ROOT/'review/2026-10-15/csv-examples';(out/'executed-results.json').write_text(json.dumps(results,indent=2)+'\n')
p=ROOT/'data/iuea_deck_content.json';decks=json.loads(p.read_text())
for d in decks:
 last_result=None
 for s in d['slides']:
  match=next((r for r in results if (r['cohort'],r['week'],r['title'],r['code'])==(d['cohort'],d['week'],s['title'],s.get('practice_code'))),None)
  if match:last_result=match
  elif s['kind']=='code' and s.get('practice_code')=='' and s.get('walkthrough_revision'):match=last_result
  if match:
   suffix=s['notes'].split('\n\nFurther explanation\n',1)
   s['notes']=s['notes'].split('\n\nOutput from the supplied CSV')[0]+'\n\nOutput from the supplied CSV (this cohort):\n'+(match['output'] or 'A chart is displayed.')+('\n\nFurther explanation\n'+suffix[1] if len(suffix)>1 else '')
   # Avoid replacing beginner syntax captions or putting an unreadable table on slides.
   if d['week']>=5 and s.get('practice_code'):
    lines=match['output'].strip().splitlines()
    if lines and len(lines)<=3 and sum(map(len,lines))<140:s['caption']='Output: '+' / '.join(lines)
    elif not lines:s['caption']='The chart uses the supplied CSV observations.'
p.write_text(json.dumps(decks,indent=2)+'\n')
print(f'Executed {len(results)} code examples across {len({(r["cohort"],r["week"]) for r in results})} decks.')
