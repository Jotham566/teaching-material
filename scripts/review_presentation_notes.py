"""Prepare a reproducible, private lecturer-note overlay for all current decks.
Run from the repository root; install with apply_presentation_notes.py after
Artifact Tool has authored the notes carriers. Does not touch student packets.
"""
from pathlib import Path
import json, shutil, hashlib
from presentation_teaching_support import make_notes, correct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'review/2026-09-21/presentation-notes'
SOURCE=ROOT/'review/2026-09-15/ppt-revision/deck-content.json'
def main():
 decks=json.loads((OUT/'inventory.json').read_text()); sources=json.loads(SOURCE.read_text());lookup={d['filename']:d for d in sources}
 records=[]
 previous=json.loads((OUT/'notes-plan.json').read_text()) if (OUT/'notes-plan.json').exists() else []
 previous_notes={d['path']:[s['notes'] for s in d['slides']] for d in previous}
 for deck in decks:
  path=ROOT/deck['path'];backup=OUT/'originals'/path.name;backup.parent.mkdir(exist_ok=True)
  if not backup.exists():shutil.copy2(path,backup)
  source=lookup.get(path.name);slides=deck['slides'];result=[]
  for i,s in enumerate(slides):
   src=source['slides'][i] if source else None
   notes=make_notes(s,slides[i-1] if i else None,slides[i+1] if i+1<len(slides) else None,src,str(path))
   result.append(dict(number=i+1,notes=notes,notes_part=s['notes_part'],visible_before=s['text'],visible_after=correct(s['text'],str(path))))
   if src:
    for key in ('title','body','caption','check','notes'):
     if isinstance(src.get(key),str):src[key]=correct(src[key],str(path))
    src['notes']=notes
  records.append(dict(path=deck['path'],before_sha256=hashlib.sha256(backup.read_bytes()).hexdigest(),slides=result))
 (OUT/'changed-note-decks.json').write_text(json.dumps([d['path'] for d in records if previous_notes.get(d['path'])!=[s['notes'] for s in d['slides']]],indent=2)+'\n')
 (OUT/'notes-plan.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 SOURCE.write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
 print(f'Prepared {len(records)} decks, {sum(len(d["slides"]) for d in records)} slide notes')
if __name__=='__main__':main()
