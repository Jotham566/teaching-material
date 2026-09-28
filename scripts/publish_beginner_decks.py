"""Install only validated, rendered PPTX files whose slide content matches the source."""
from pathlib import Path
import json,zipfile,re,hashlib,shutil,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';R=ROOT/'review/2026-09-15/ppt-revision'
D=json.loads((R/'deck-content.json').read_text());A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
norm=lambda s:re.sub(r'\s+',' ',s).strip()
def xml_text(xml):
 # Formatting runs can split a Python token (for example else and its colon).
 # Only paragraph boundaries introduce a separator; run boundaries do not.
 return '\n'.join(''.join(e.text or '' for e in p.iter(A+'t')) for p in ET.fromstring(xml).iter(A+'p'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matches(path,d):
 try:
  z=zipfile.ZipFile(path);names=sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+.xml',n)],key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1)))
  if len(names)!=len(d['slides']):return False
  for n,s in zip(names,d['slides']):
   text=norm(xml_text(z.read(n)))
   # Numbered layouts insert editable step numbers between paragraphs. Validate
   # each original paragraph, plus the native table and vocabulary content.
   required_text=[s['title'],s.get('code',''),s.get('caption',''),s.get('check','')]
   required_text+=re.split(r'\n\s*\n',s.get('body',''))
   required_text+=[str(cell) for row in s.get('table',[]) for cell in row]
   required_text+=[item[key] for item in s.get('concepts',[]) for key in ('term','meaning')]
   if s.get('kind')=='code':
    cues=s.get('explain',[])
    required_text+=cues if max(map(len,s['code'].split('\n')))<=44 else cues[:1]
   for required in required_text:
    if required and norm(required) not in text:return False
   if s.get('image'):
    expected=hashlib.sha256((ROOT/s['image']).read_bytes()).hexdigest()
    if not any(hashlib.sha256(z.read(m)).hexdigest()==expected for m in z.namelist() if m.startswith('ppt/media/')):return False
   num=re.search(r'(\d+)\.xml',n).group(1)
   notes=xml_text(z.read('ppt/notesSlides/notesSlide'+num+'.xml'))
   if norm(s.get('notes','')) not in norm(notes):return False
   if s.get('url'):
    rel=z.read('ppt/slides/_rels/slide'+num+'.xml.rels').decode();
    if s['url'].replace('&','&amp;') not in rel:return False
  return True
 except (KeyError,zipfile.BadZipFile):return False
selected=[]
for d in D:
 choices=sorted((R/'final').glob('*/'+d['filename']),key=lambda p:p.stat().st_mtime,reverse=True)
 match=next((p for p in choices if matches(p,d)),None)
 if match is None:raise RuntimeError('No matching final edition: '+d['filename'])
 build=R/'build'/match.parent.name/d['filename'].replace('.pptx','');receipt=json.loads((build/'validation.json').read_text())
 assert receipt['finalSha256']==sha(match)
 assert len(list((build/'render').glob('slide-*.png')))==len(d['slides'])
 selected.append((d,match,build))
backup=R/'original-decks';backup.mkdir(exist_ok=True)
original={}
for p in (BASE/'decks').glob('*.pptx'):
 original[p.name]=sha(p)
 if not(backup/p.name).exists():shutil.copy2(p,backup/p.name)
manifest=[]
for d,p,build in selected:
 shutil.copy2(p,BASE/'decks'/d['filename'])
 manifest.append({'cohort':d['cohort'],'week':d['week'],'filename':d['filename'],'slides':len(d['slides']),'sha256':sha(p),'edition':p.parent.name,'render':str((build/'render').relative_to(ROOT)),'assessments':d['assessment_ids'],'quiz':d['quiz_url']})
for name,checksum in original.items():
 if not any(d['filename']==name for d in D):assert sha(BASE/'decks'/name)==checksum
(R/'published-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
text=['# PowerPoint teaching decks','','Teach directly from the PowerPoints below. Open Presenter View for the teaching prompts and practice explanations. All decks include reviewed lecturer notes; completed lessons retain their existing visual design.','','Use the matching student ZIP for practice and the issued assignment. The final slides contain the cohort quiz and submission links. Quizzes remain available for 24 hours from activation. Assignment windows use their separately published dates.','','| Week | CML3111 | CML3112 | CML3113 |','|---|---|---|---|']
for w in range(2,16):
 cells=[str(w)]
 for c in ('CML3111','CML3112','CML3113'):
  d=next((x for x in D if x['cohort']==c and x['week']==w),None)
  cells.append(f'[Week {w}]({d["filename"]})' if d else 'Completed teaching')
 text.append('| '+' | '.join(cells)+' |')
text+=['','[All presentations and lecturer notes](LECTURER_NOTES_INDEX.md)','','[Curriculum benchmark and teaching map](../Curriculum_Benchmark_and_Teaching_Map.md)','','[Lecturer quick guide](../IUEA_ML_Beginner_Teaching_Quick_Guide.docx) · [Detailed guidance](../Beginner_Lecturer_Guide.md)','','Video links open externally and need internet. Preview the selected short excerpt before class. Major assessments retain their separate grading-release checks.']
(BASE/'decks/README.md').write_text('\n'.join(text)+'\n')
(BASE/'decks/READ_BEFORE_TEACHING.md').write_text('# Teaching materials\n\nUse the updated PowerPoints in this folder. See [the deck index](README.md). Speaker notes provide the worked explanations. The HTML lesson route is retired.\n')
print(f'Installed {len(manifest)} matching validated decks with {sum(x["slides"] for x in manifest)} rendered slides. Original decks retained in private review archive.')
