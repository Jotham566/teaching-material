"""Stage native notes only; preserve every non-note ZIP part byte for byte."""
from pathlib import Path
import copy,hashlib,json,shutil,zipfile,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'review/2026-09-29/slide-specific-notes'
P='{http://schemas.openxmlformats.org/presentationml/2006/main}';A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
E.register_namespace('a',A[1:-1]);E.register_namespace('p',P[1:-1])
def body(root):
 for sp in root.iter(P+'sp'):
  ph=sp.find('.//'+P+'ph')
  if ph is not None and ph.get('type')=='body':return sp
 raise ValueError('No note body')
def note_text(root):return '\n'.join(''.join(t.text or '' for t in p.iter(A+'t')) for p in body(root).iter(A+'p')).strip()
def main():
 plans=json.loads((R/'notes-plan.json').read_text());rows=[]
 for d in plans:
  source=ROOT/d['path'];original=R/'originals'/source.name;candidate=R/'candidates'/source.name
  original.parent.mkdir(exist_ok=True);candidate.parent.mkdir(exist_ok=True)
  assert hashlib.sha256(source.read_bytes()).hexdigest()==d['sha256'],'Source changed during note authoring: '+str(source)
  if not original.exists():shutil.copy2(source,original)
  # Keep the first pre-edit backup across editorial repair passes. Visible parts
  # are separately checked against the current source below.
  with zipfile.ZipFile(source) as z,zipfile.ZipFile(R/'authored'/source.name) as authored:
   edits={}
   for s in d['slides']:
    original_note=E.fromstring(z.read(s['notes_part']));replacement=E.fromstring(authored.read(f'ppt/notesSlides/notesSlide{s["number"]}.xml'))
    target=body(original_note);target.remove(target.find(P+'txBody'));target.append(copy.deepcopy(body(replacement).find(P+'txBody')))
    assert note_text(original_note)==s['notes'].strip()
    edits[s['notes_part']]=E.tostring(original_note,encoding='utf-8',xml_declaration=True)
   with zipfile.ZipFile(candidate,'w',zipfile.ZIP_DEFLATED) as final:
    for item in z.infolist():final.writestr(item,edits.get(item.filename,z.read(item.filename)))
  with zipfile.ZipFile(source) as old,zipfile.ZipFile(candidate) as new:
   assert old.namelist()==new.namelist()
   assert new.testzip() is None
   for part in old.namelist():
    if part not in edits:assert old.read(part)==new.read(part),part
   for part in new.namelist():
    if part.endswith(('.xml','.rels')):E.fromstring(new.read(part))
  rows.append(dict(path=d['path'],slides=len(d['slides']),sha256=hashlib.sha256(candidate.read_bytes()).hexdigest(),non_note_parts_byte_identical=True))
 (R/'staged.json').write_text(json.dumps(rows,indent=2)+'\n')
 print('Staged',len(rows),'decks; all slide artwork, media, links and layout parts remain byte-identical.')
if __name__=='__main__':main()
