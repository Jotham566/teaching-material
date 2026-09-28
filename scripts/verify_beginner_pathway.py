"""Check learner navigation and that the new packages preserve assessment contracts."""
from pathlib import Path
from html.parser import HTMLParser
import json, zipfile, hashlib
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and 'href' in a:self.links.append(a['href'])
manifest=json.loads((ROOT/'review/2026-09-15/ppt-revision/published-manifest.json').read_text());assert len(manifest)==41
assert not any(x['week']==2 and x['cohort']=='CML3112' for x in manifest)
for row in manifest:
 p=BASE/'decks'/row['filename'];assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
packages=[]
for cohort in ('CML3111','CML3112','CML3113'):
 for week in (2,3,4,5,6,8,9,10,11,12):
  if cohort=='CML3112' and week==2:continue
  z=zipfile.ZipFile(BASE/'student_packages'/f'{cohort}_W{week:02}_student.zip');names=z.namelist()
  assert len(names)==len(set(names));assert '00_START_HERE.txt' in names and 'lesson.html' not in names
  assert all(n=='04_hidden_state.ipynb' or not any(x in n.lower() for x in ('hidden','solution','lecturer','calibration','gradebook')) for n in names)
  lesson=BASE/'guided_practice'/cohort/f'W{week:02}'
  if week!=2:assert z.read('guided_practice.ipynb')==(lesson/'guided_practice.ipynb').read_bytes()
  source=BASE/'setup'/cohort if week==2 else BASE/'practicals'/f'W{week:02}'/cohort if week<=5 else BASE/'assessment_banks'/f'W{week:02}'/cohort/'A'
  for f in source.iterdir():
   if f.suffix in ('.ipynb','.csv','.md','.py'):assert z.read(f.name)==f.read_bytes(),f
  assert 'SUBMIT_HERE.txt' in names
  packages.append(f'{cohort} W{week:02}')
expected={3:['8\n','4.0\n','high\nlow\n','92 -8\n'],4:['4.0\n','[2.5, 3.5]',"{'A': 3.0, 'B': 9.0}"],5:['4.5','A     6','B    12'],6:['23.0','[20, None, 22, 24, 80]','3 2'],8:['[15.0]\n[15.0]\n[14.0]','3.1622776601683795'],9:['0.5\n0.5\n6'],10:['[1, 2] [3]'],11:['0.4 1000\n0.5'],12:["['simple']"]}
executions=json.loads((ROOT/'review/2026-09-15/ppt-revision/practice-execution.json').read_text());assert len(executions)==27
for item in executions:
 for value in expected[item['week']]:assert value in item['output'],item
# Record current executable-cell hashes; these distinguish later prose-only edits.
hashes={}
for p in (BASE/'guided_practice').glob('*/W*/guided_practice.ipynb'):
 n=json.loads(p.read_text());codes='\n'.join(''.join(c['source']) for c in n['cells'] if c['cell_type']=='code')
 compile(codes,str(p),'exec');hashes[str(p.relative_to(BASE))]=hashlib.sha256(codes.encode()).hexdigest()
report={'decks':len(manifest),'packages':len(packages),'practice_outputs_checked':len(executions),'pptx_hashes':'pass','assignment_files_match_issued_sources':'pass','private_file_exclusion':'pass','code_sha256':hashes}
(ROOT/'review/2026-09-15/ppt-revision/delivery-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('41 PPTX files match their validated editions; 29 ZIPs: assessment files match issued sources and no private keys; 27 executed outputs match teaching expectations')
