"""Publish the validated speaker-note edition in place, with source protection."""
from pathlib import Path
import hashlib,json,shutil,zipfile
from reviewed_notes_overlay import signature
ROOT=Path(__file__).resolve().parents[1];R=ROOT/'review/2026-09-29/slide-specific-notes'
plans=json.loads((R/'notes-plan.json').read_text());staged=json.loads((R/'staged.json').read_text())
source_path=ROOT/'data/iuea_deck_content.json';sources=json.loads(source_path.read_text());lookup={d['filename']:d for d in sources};overlay={};report=[]
for d in plans:
 dest=ROOT/d['path'];name=dest.name;final=R/'validated'/name
 receipt=json.loads((R/'validation'/dest.stem/'validation.json').read_text())
 digest=hashlib.sha256(final.read_bytes()).hexdigest()
 assert receipt['finalSha256']==digest
 assert digest==next(r['sha256'] for r in staged if r['path']==d['path'])
 assert hashlib.sha256(dest.read_bytes()).hexdigest()==d['sha256'],'Source was edited during validation'
 with zipfile.ZipFile(dest) as old,zipfile.ZipFile(final) as new:
  notes={s['notes_part'] for s in d['slides']}
  assert old.namelist()==new.namelist()
  assert all(old.read(n)==new.read(n) for n in old.namelist() if n not in notes)
 shutil.copy2(final,dest)
 md=dest.parent/'lecturer_notes'/f'{dest.stem}.md';md.parent.mkdir(exist_ok=True)
 md.write_text('# '+dest.stem.replace('_',' ')+'\n\nLecturer companion. The same explanations are embedded in the PowerPoint speaker notes. Open Presenter View, or expand the Notes pane when preparing.\n\n'+'\n\n'.join(f'## Slide {s["number"]} — {s["heading"]}\n\n{s["notes"]}' for s in d['slides'])+'\n')
 if name in lookup:
  src=lookup[name];assert len(src['slides'])==len(d['slides'])
  for a,b in zip(src['slides'],d['slides']):a['notes']=b['notes']
  overlay[name]=[dict(signature=signature(s),notes=s['notes']) for s in src['slides']]
 report.append(dict(filename=name,slides=len(d['slides']),sha256=digest,notes_only=True))
source_path.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
(ROOT/'data/slide_specific_lecturer_notes.json').write_text(json.dumps(overlay,ensure_ascii=False,indent=2)+'\n')
manifest_path=ROOT/'data/iuea_foundations_manifest.json';manifest=json.loads(manifest_path.read_text());hashes={r['filename']:r['sha256'] for r in report}
for row in manifest:row['sha256']=hashes[row['filename']]
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
(ROOT/'data/iuea_lecturer_notes_manifest.json').write_text(json.dumps(report,indent=2)+'\n')
index=ROOT/'IUEA_Teaching_Plan/decks/LECTURER_NOTES_INDEX.md'
lines=['# Lecture slides and speaker notes','','Each slide has its own explanation, teaching illustration and misconception guidance. Code slides include a line-by-line explanation. The `.md` companion contains the same notes for preparation away from PowerPoint.','','Close and reopen an already open presentation to load the updated notes. Use **View → Notes** while preparing or **Slide Show → Presenter View** when teaching. Speaker notes are for the lecturer; the audience display shows the slide.','','## Current next lessons','','CML3112: Week 4. CML3111 and CML3113: Week 3, from slide 1.','','## All weeks','']
for row in report:
 name=row['filename'];lines.append(f'- [{name}](./{name}) · [Readable notes](./lecturer_notes/{Path(name).stem}.md)')
index.write_text('\n'.join(lines)+'\n')
(R/'published.json').write_text(json.dumps(report,indent=2)+'\n')
print('Published',len(report),'decks and',sum(r['slides'] for r in report),'slide-specific notes.')
