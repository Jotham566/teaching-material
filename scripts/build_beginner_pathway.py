"""Build practice directly from the reviewed PowerPoint sequence.

No independently ordered lesson exists: both artifacts share deck-content.json.
A multi-slide program becomes one runnable notebook cell. Questions stay in text
cells, so Run all checks worked examples without filling in student exercises.
"""
from pathlib import Path
import json,sys,subprocess
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';OUT=BASE/'guided_practice'
REVIEW=ROOT/'review/2026-09-15/ppt-revision'
decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text());checks=[];count=0
for deck in decks:
 week=deck['week'];cohort=deck['cohort']
 if '--only' in sys.argv and f'{cohort}-W{week:02}'!=sys.argv[sys.argv.index('--only')+1]:continue
 if week not in (2,3,4,5,6,7,8,9,10,11,12,13,14,15):continue
 if '--later-only' in sys.argv and week<6:continue
 if '--csv-only' in sys.argv and not deck.get('csv_examples_revision'):continue
 folder=OUT/cohort/f'W{week:02}';folder.mkdir(parents=True,exist_ok=True)
 cells=[('markdown',f'# Week {week} guided practice\n{cohort}. Follow the lecturer’s PowerPoint in this order. This notebook contains worked examples, not your graded upload.\n\nExtract the student ZIP and keep its files together. For file-reading examples, upload the supplied CSV into the Colab runtime before running the file-reading example. From the file-reading lesson onward, worked table examples use the supplied CSV. Earlier syntax examples introduce Python before file access.\n')]
 if week==6 and cohort in ('CML3112','CML3113'):
  cells[0]=('markdown',cells[0][1]+'\n**A6 and Quiz 6 are waived. This is ungraded practice. No submission is required.**\n')
 for slide in deck['slides']:
  if slide['title'] in ('Your issued assignment','Your issued task','Ungraded cleaning practice'):break
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
  if slide['kind']=='code':
   program=slide.get('practice_code',slide['code'])
   if week==2 and '# Run the next two lines in a SECOND cell.' in program:
    setup,repeat=program.split('# Run the next two lines in a SECOND cell.',1)
    cells.append(('code',setup.strip()+'\n'))
    cells.append(('markdown','Run the setup cell once. Run the next cell once for 17, then again for 22. Restart and run all to return to 17.\n'))
    cells.append(('code',repeat.strip()+'\n'))
   else:cells.append(('code',program+'\n'))
   if slide.get('expected_output'):
    cells.append(('markdown','**Example output** (timings and display formatting may vary)\n\n```text\n'+slide['expected_output']+'\n```\n'))
 if week==6 and cohort in ('CML3112','CML3113'):
  cells.append(('markdown','## Save your practice\nA6 and Quiz 6 are waived. No submission is required. Restart and run all cells, then save in Drive. Continue with the Test 1 revision PDF and matching practice CSV in a new notebook.\n'))
 elif week in (13,15):
  cells.append(('markdown','## Continue your project preparation\nUse the published project and presentation requirements in the slides. This notebook is a revision aid, not an additional weekly assignment. Keep the required submission files and deadlines.\n'))
 elif week==14:
  cells.append(('markdown','## Save your revision\nThis practice is ungraded. Save your notebook in Drive. On test day, download the separate test notebook and CSV from the test entry page in the slides.\n'))
 elif week in (13,15):
  cells.append(('markdown','## Continue your project preparation\nUse the published project and presentation requirements in the slides. This notebook is a revision aid, not an additional weekly assignment. Keep the required submission files and deadlines.\n'))
 elif week==14:
  cells.append(('markdown','## Save your revision\nThis practice is ungraded. Save your notebook in Drive. On test day, download the separate test notebook and CSV from the test entry page in the slides.\n'))
 else:
  cells.append(('markdown','## Continue with your issued assignment\nOpen the assignment notebook named in 00_START_HERE.txt. Keep required function names, return types and units. guided_practice.ipynb is not a graded upload. Use SUBMIT_HERE.txt for the correct submission link.\n'))
 nb={'cells':[{'cell_type':kind,'metadata':{},**({'execution_count':None,'outputs':[]} if kind=='code' else {}),'source':t.splitlines(keepends=True)} for kind,t in cells],'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'}},'nbformat':4,'nbformat_minor':5}
 (folder/'guided_practice.ipynb').write_text(json.dumps(nb,indent=2)+'\n');count+=1
 if '--verify' in sys.argv:
  program='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
  args=['docker','run','--rm','--network=none']
  if week in (4,5):args+=['--mount',f'type=bind,src={BASE}/practicals/W{week:02}/{cohort},dst=/data,readonly','--workdir','/data']
  if week>=6:
   source_week={7:6,14:12}.get(week,week)
   data_folder=BASE/f'assessment_banks/W{source_week:02}/{cohort}/A'
   if not data_folder.exists():data_folder=BASE/f'assessment_banks/TEST1/{cohort}/A'
   args+=['--mount',f'type=bind,src={data_folder},dst=/data,readonly','--workdir','/data','-e','MPLBACKEND=Agg']
  r=subprocess.run(args+['iuea-notebooks:2026.09','python','-c',program],capture_output=True,text=True)
  if r.returncode:raise RuntimeError(f'{cohort} W{week}: {r.stderr}')
  checks.append({'week':week,'cohort':cohort,'output':r.stdout})
if checks:(REVIEW/'practice-execution.json').write_text(json.dumps(checks,indent=2)+'\n')
print(f'Built {count} guided notebooks from the slide order; executed {len(checks)}.')
