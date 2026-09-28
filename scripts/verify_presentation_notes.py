"""Verify installed slide-to-note relationships, note contents and publication hashes."""
import hashlib,json,posixpath,zipfile,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'review/2026-09-21/presentation-notes'
NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
def main():
 plan=json.loads((R/'notes-plan.json').read_text());installed=json.loads((R/'installation.json').read_text());checks=json.loads((R/'validation-progress.json').read_text());total=0
 assert len(plan)==len(installed)==len(checks)==60
 for deck in plan:
  path=ROOT/deck['path'];digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest==next(d['sha256'] for d in installed if d['path']==deck['path'])
  receipt=json.loads((R/'validation'/path.stem/'validation.json').read_text());assert receipt['finalSha256']==digest
  with zipfile.ZipFile(path) as z:
   assert z.testzip() is None
   for s in deck['slides']:
    rel=E.fromstring(z.read(f'ppt/slides/_rels/slide{s["number"]}.xml.rels'));links=[r for r in rel if r.get('Type','').endswith('/notesSlide')];assert len(links)==1
    part=posixpath.normpath(posixpath.join('ppt/slides',links[0].get('Target'))).lstrip('/');root=E.fromstring(z.read(part))
    bodies=[sp for sp in root.findall('.//p:sp',NS) if sp.find('.//p:ph',NS) is not None and sp.find('.//p:ph',NS).get('type')=='body'];assert len(bodies)==1
    text='\n'.join(''.join(t.text or '' for t in p.findall('.//a:t',NS)) for p in bodies[0].findall('.//a:p',NS))
    assert text.strip()==s['notes'].strip(),(path,s['number']);total+=1
 assert sum(len(d['fit_flags']) for d in checks)==0
 result={'presentations':60,'slides_with_exact_verified_notes':total,'cumulative_visible_corrections':sum(len(d['visible_edits']) for d in installed),'finalizer_receipts_and_hashes':'pass','note_relationships_and_content':'pass','changed_slide_fit_flags':0,'native_powerpoint_ui_test':False}
 (R/'final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
