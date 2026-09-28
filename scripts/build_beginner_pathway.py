"""Build practice directly from the reviewed PowerPoint sequence.

No independently ordered lesson exists: both artifacts share deck-content.json.
A multi-slide program becomes one runnable notebook cell. Questions stay in text
cells, so Run all checks worked examples without filling in student exercises.
"""
from pathlib import Path
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';OUT=BASE/'guided_practice'
REVIEW=ROOT/'review/2026-09-15/ppt-revision'
decks=json.loads((REVIEW/'deck-content.json').read_text());checks=[];count=0
for deck in decks:
 week=deck['week'];cohort=deck['cohort']
 if week not in (3,4,5,6,8,9,10,11,12):continue
 folder=OUT/cohort/f'W{week:02}';folder.mkdir(parents=True,exist_ok=True)
 cells=[('markdown',f'# Week {week} guided practice\n{cohort}. Follow the lecturer’s PowerPoint in this order. This notebook contains worked examples, not your graded upload.\n\nExtract the student ZIP and keep its files together. For Weeks 4 and 5, upload the supplied CSV into the Colab runtime before running the file-reading example. Small worked datasets are invented; the CSV inspection uses your supplied file.\n')]
 for slide in deck['slides']:
  if slide['title'] in ('Your issued assignment','Your issued task'):break
  if slide['kind']=='cover':continue
  if slide['kind']=='code' and slide.get('practice_code')=='':continue
  text='## '+slide['title']+f"\n*PowerPoint slide {slide['sequence_number']}*\n\n"
  text+=slide.get('body','')+'\n'
  if 'concepts' in slide:text+='\n\n'.join('**'+x['term']+'** — '+x['meaning'] for x in slide['concepts'])+'\n'
  if 'table' in slide:
   table=['| '+' | '.join(str(c) for c in row)+' |' for row in slide['table']]
   table.insert(1,'| '+' | '.join('---' for _ in slide['table'][0])+' |');text+='\n'+'\n'.join(table)+'\n'
  if slide.get('kind') in ('scene','figure'):text+='See the illustration on this PowerPoint slide.\n'
  text+='\n'+slide.get('caption','')+'\n'
  if slide.get('url'):text+='\n['+slide['label']+']('+slide['url']+')\n'
  cells.append(('markdown',text))
  if slide['kind']=='code':cells.append(('code',slide['practice_code']+'\n'))
 cells.append(('markdown','## Continue with your issued assignment\nOpen the assignment notebook named in 00_START_HERE.txt. Keep required function names, return types and units. guided_practice.ipynb is not a graded upload. Use SUBMIT_HERE.txt for the correct submission link.\n'))
 nb={'cells':[{'cell_type':kind,'metadata':{},**({'execution_count':None,'outputs':[]} if kind=='code' else {}),'source':t.splitlines(keepends=True)} for kind,t in cells],'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},'nbformat':4,'nbformat_minor':5}
 (folder/'guided_practice.ipynb').write_text(json.dumps(nb,indent=2)+'\n');count+=1
 if '--verify' in sys.argv:
  program='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
  args=['docker','run','--rm','--network=none']
  if week in (4,5):args+=['--mount',f'type=bind,src={BASE}/practicals/W{week:02}/{cohort},dst=/data,readonly','--workdir','/data']
  r=subprocess.run(args+['iuea-notebooks:2026.09','python','-c',program],capture_output=True,text=True)
  if r.returncode:raise RuntimeError(f'{cohort} W{week}: {r.stderr}')
  checks.append({'week':week,'cohort':cohort,'output':r.stdout})
if checks:(REVIEW/'practice-execution.json').write_text(json.dumps(checks,indent=2)+'\n')
print(f'Built {count} guided notebooks from the slide order; executed {len(checks)}.')
