"""Verify the published Week 3–15 teaching edition, notes and student ZIPs.

Run after prepare/build/publish. No private review directory is required.
"""
from pathlib import Path
import hashlib,json,posixpath,re,zipfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
D=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
M=json.loads((ROOT/'data/iuea_foundations_manifest.json').read_text())
def norm(s):return re.sub(r'\s+',' ',s).strip()
def text(xml):return '\n'.join(''.join(t.text or '' for t in p.iter(A+'t')) for p in ET.fromstring(xml).iter(A+'p'))
assert len(M)==39
slide_count=0
for row in M:
 d=next(d for d in D if d['filename']==row['filename'])
 p=BASE/'decks'/row['filename']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'],p
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for i,s in enumerate(d['slides'],1):
   actual=text(z.read(f'ppt/slides/slide{i}.xml'))
   assert norm(s['title']) in norm(actual),(p,i)
   assert not re.search(r'partner|swap roles|try it together|make four cards|peer feedback',actual,re.I),(p,i)
   rels=ET.fromstring(z.read(f'ppt/slides/_rels/slide{i}.xml.rels'))
   notes=[r for r in rels if r.get('Type','').endswith('/notesSlide')];assert len(notes)==1
   part=posixpath.normpath(posixpath.join('ppt/slides',notes[0].get('Target'))).lstrip('/')
   assert norm(s['notes']) in norm(text(z.read(part))),(p,i)
   for value in [s.get('code',''),s.get('caption','')]+s.get('body','').split('\n\n'):
    if value:assert norm(value) in norm(actual),(p,i,value)
   slide_count+=1
 companion=(BASE/'decks/lecturer_notes'/Path(row['filename']).with_suffix('.md')).read_text()
 assert len(re.findall(r'^## Slide ',companion,re.M))==len(d['slides'])
 for i,s in enumerate(d['slides'],1):assert f'## Slide {i} — '+s['title'] in companion
packages=0
for cohort in ('CML3111','CML3112','CML3113'):
 for week in (3,4,5,6,8,9,10,11,12):
  with zipfile.ZipFile(BASE/'student_packages'/f'{cohort}_W{week:02}_student.zip') as z:
   names=z.namelist();assert len(names)==len(set(names))
   assert '00_START_HERE.txt' in names and 'SUBMIT_HERE.txt' in names
   assert all(not any(x in n.lower() for x in ('hidden','solution','lecturer','calibration','gradebook','lesson.html')) for n in names)
   nb=BASE/'guided_practice'/cohort/f'W{week:02}'/'guided_practice.ipynb'
   assert z.read('guided_practice.ipynb')==nb.read_bytes()
   source=BASE/'practicals'/f'W{week:02}'/cohort if week<=5 else BASE/'assessment_banks'/f'W{week:02}'/cohort/'A'
   for f in source.iterdir():
    if f.suffix in ('.ipynb','.csv','.md','.py'):assert z.read(f.name)==f.read_bytes(),f
  packages+=1
print(f'{len(M)} decks / {slide_count} slides: hashes, visible source text, linked speaker notes and lecturer companions match.')
print(f'{packages} student ZIPs: current guided notebooks, unchanged issued assignment files, no private grading files.')
