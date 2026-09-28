"""Publish validated foundations decks and matching lecturer notes."""
from pathlib import Path
import json,hashlib,shutil,zipfile,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan';R=ROOT/'review/2026-09-15/ppt-revision'
D=json.loads((ROOT/'data/iuea_deck_content.json').read_text());A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
def norm(t):return re.sub(r'\s+',' ',t).strip()
def text(xml):return '\n'.join(''.join(t.text or '' for t in p.iter(A+'t')) for p in ET.fromstring(xml).iter(A+'p'))
manifest=[]
for d in D:
 if d['week']<3:continue
 edition='explicit-foundations-final-20260929' if d['week'] in (3,4,6,8,9,11) else 'explicit-foundations-20260929'
 final=R/'final'/edition/d['filename'];build=R/'build'/edition/Path(d['filename']).stem
 receipt=json.loads((build/'validation.json').read_text())
 assert receipt['finalSha256']==hashlib.sha256(final.read_bytes()).hexdigest()
 assert len(list((build/'render').glob('slide-*.png')))==len(d['slides'])
 with zipfile.ZipFile(final) as z:
  for i,s in enumerate(d['slides'],1):
   actual=text(z.read(f'ppt/slides/slide{i}.xml'))
   assert norm(s['title']) in norm(actual),(d['filename'],i)
   assert not re.search(r'partner|swap roles|try it together|make four cards',actual,re.I),(d['filename'],i,'live group instruction')
   assert norm(s['notes']) in norm(text(z.read(f'ppt/notesSlides/notesSlide{i}.xml')))
   for value in [s.get('code',''),s.get('caption','')]+s.get('body','').split('\n\n'):
    if value:assert norm(value) in norm(actual),(d['filename'],i,value)
 shutil.copy2(final,BASE/'decks'/d['filename'])
 notes=['# '+d['filename'].replace('_',' ').replace('.pptx',''),'','Lecturer companion to the revised PowerPoint. Slide numbers match this edition. Explain the worked examples directly; revision checks are for individual study.','']
 for i,s in enumerate(d['slides'],1):notes+=['## Slide '+str(i)+' — '+s['title'],'',s['notes'],'']
 (BASE/'decks/lecturer_notes'/Path(d['filename']).with_suffix('.md')).write_text('\n'.join(notes).rstrip()+'\n')
 manifest.append({'cohort':d['cohort'],'week':d['week'],'filename':d['filename'],'slides':len(d['slides']),'sha256':receipt['finalSha256'],'edition':edition,'render':str((build/'render').relative_to(ROOT))})
(ROOT/'data/iuea_foundations_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Published',len(manifest),'validated decks and lecturer companions')
