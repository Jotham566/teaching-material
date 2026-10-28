"""Verify the single current teaching edition; optionally export one teacher ZIP."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E
import hashlib,json,re,sys
from course_paths import ROOT,MAINTENANCE,DOCUMENTS

def package():
 manifest=json.loads((MAINTENANCE/'Deck Manifest.json').read_text())
 assert len(manifest)==12
 assert len(list((ROOT/'02 Class Slides').glob('*.pptx')))==len(manifest)
 total=0
 for item in manifest:
  p=ROOT/item['file']
  with ZipFile(p) as z:
   assert z.testzip() is None
   slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)]
   assert len(slides)==item['slides']
   for n in slides:assert E.fromstring(z.read(n)).get('show','1')!='0'
   total+=len(slides)
  receipt=json.loads((MAINTENANCE/'Validation'/f"Session {item['session']:02}.json").read_text())
  assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt['finalSha256']
 for p in DOCUMENTS.values():
  assert p.is_file()
  with ZipFile(p) as z:assert z.testzip() is None
 hashes=json.loads((MAINTENANCE/'File Integrity.json').read_text())
 for rel,h in hashes.items():assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,rel
 print(f'Verified {len(manifest)} current decks, {total} visible slides, {len(DOCUMENTS)} course documents and all recorded hashes.')
 if '--zip' not in sys.argv:return
 exports=ROOT/'Exports';exports.mkdir(exist_ok=True);target=exports/'Applied AI and Automation - Teacher Pack.zip'
 with ZipFile(target,'w',ZIP_DEFLATED) as z:
  for f in sorted(ROOT.rglob('*')):
   rel=f.relative_to(ROOT)
   if not f.is_file() or rel.parts[0]=='Exports' or any(p.startswith('.') or p=='__pycache__' for p in rel.parts):continue
   z.write(f,str(Path(ROOT.name)/rel))
 with ZipFile(target) as z:assert z.testzip() is None
 print(target)
if __name__=='__main__':package()
