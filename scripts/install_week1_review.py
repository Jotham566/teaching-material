"""Install Artifact-authored notes while preserving Week 1 media and geometry."""
import json,copy,zipfile,posixpath,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'review/2026-10-20/full-course-review'
A='{http://schemas.openxmlformats.org/drawingml/2006/main}';P='{http://schemas.openxmlformats.org/presentationml/2006/main}'
def tx(root):
 for shape in root.iter(P+'sp'):
  ph=shape.find('.//'+P+'ph')
  if ph is not None and ph.get('type')=='body':return shape,shape.find(P+'txBody')
 raise ValueError('Missing notes body')
for d in json.loads((OUT/'week1-review-plan.json').read_text()):
 with zipfile.ZipFile(OUT/'originals'/d['filename']) as z:files={n:z.read(n) for n in z.namelist()}
 unchanged={n:b for n,b in files.items() if n.startswith('ppt/media/')}
 for name,xml in d['replacements'].items():files[name]=xml.encode()
 with zipfile.ZipFile(OUT/'authored'/d['filename']) as authored:
  for s in d['slides']:
   rel=E.fromstring(files[f"ppt/slides/_rels/slide{s['number']}.xml.rels"])
   target_path=next(r.get('Target') for r in rel if r.get('Type','').endswith('/notesSlide'))
   name=posixpath.normpath(posixpath.join('ppt/slides',target_path))
   target=E.fromstring(files[name]);shape,old=tx(target)
   _,new=tx(E.fromstring(authored.read(f"ppt/notesSlides/notesSlide{s['number']}.xml")))
   shape.remove(old);shape.append(copy.deepcopy(new));files[name]=E.tostring(target,encoding='utf-8',xml_declaration=True)
 assert all(files[n]==b for n,b in unchanged.items())
 dest=ROOT/'IUEA_Teaching_Plan/decks'/d['filename']
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
  for n,b in files.items():z.writestr(n,b)
 (dest.parent/'lecturer_notes'/dest.with_suffix('.md').name).write_text('# Week 1 lecturer explanations\n\n'+'\n\n'.join(f"## Slide {s['number']}\n\n{s['notes']}" for s in d['slides']))
 print('Updated',d['filename'],'with original media preserved.')
