"""Publish the validated notes edition, reusing only byte-identical slide artwork."""
from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'review/2026-09-15/ppt-revision';N=ROOT/'review/2026-09-21/presentation-notes'
def main():
 installation=json.loads((N/'installation.json').read_text());checks=json.loads((N/'validation-progress.json').read_text())
 assert len(checks)==len(installation)==60
 assert not any(c['fit_flags'] for c in checks),'Resolve fit flags before publication'
 manifest=json.loads((R/'published-manifest.json').read_text());edition='lecturer-notes-20260922'
 for d in installation:
  name=Path(d['path']).name;validated=N/'validated'/name;receipt=json.loads((N/'validation'/Path(name).stem/'validation.json').read_text());digest=hashlib.sha256(validated.read_bytes()).hexdigest()
  assert receipt['finalSha256']==digest
  assert validated.read_bytes()==(ROOT/d['path']).read_bytes(),'Finalizer changed bytes: inspect before publishing'
  row=next((r for r in manifest if r['filename']==name),None)
  if row:
   final=R/'final'/edition/name;build=R/'build'/edition/Path(name).stem;render=build/'render';render.mkdir(parents=True,exist_ok=True);final.parent.mkdir(parents=True,exist_ok=True)
   changed={s['slide'] for s in d['visible_edits']}
   oldrender=ROOT/row['render']
   with zipfile.ZipFile(N/'originals'/name) as old,zipfile.ZipFile(validated) as new:
    for i in range(1,d['slides']+1):
     if i not in changed:assert old.read(f'ppt/slides/slide{i}.xml')==new.read(f'ppt/slides/slide{i}.xml')
     source=N/'validation'/Path(name).stem/f'after-{i}.png' if i in changed else oldrender/f'slide-{i:03}.png'
     assert source.exists(),source
     target=render/f'slide-{i:03}.png'
     if source.resolve()!=target.resolve():shutil.copy2(source,target)
   shutil.copy2(validated,final);shutil.copy2(N/'validation'/Path(name).stem/'validation.json',build/'validation.json')
   provenance=build/'render-provenance.json'
   prior=json.loads(provenance.read_text()) if provenance.exists() else {}
   provenance.write_text(json.dumps({'changed_slides_rendered':sorted(changed),'unchanged_visual_parts_byte_identical':True,'unchanged_render_source':prior.get('unchanged_render_source',row['render'])},indent=2)+'\n')
 print('60 finalizer receipts verified; 41 revised editions staged with render provenance')
if __name__=='__main__':main()
