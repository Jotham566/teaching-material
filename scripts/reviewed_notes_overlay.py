"""Keep approved lecturer notes when rebuilding the reviewed IUEA slide sequence.
Reject changed teaching content instead of silently attaching stale notes.
"""
from pathlib import Path
import hashlib,json
from presentation_teaching_support import correct
ROOT=Path(__file__).resolve().parents[1]
KEYS=('kind','title','body','caption','code','practice_code','table','concepts','url','check','explain')
def signature(slide):
 return hashlib.sha256(json.dumps({k:slide[k] for k in KEYS if k in slide},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def apply_reviewed_notes(slides,filename):
 path=ROOT/'data/reviewed_presentation_notes.json'
 if not path.exists():return
 approved=json.loads(path.read_text()).get(filename)
 if not approved:return
 if len(slides)!=len(approved):raise ValueError(f'Review lecturer notes for changed slide count: {filename}')
 for i,(s,a) in enumerate(zip(slides,approved),1):
  for k in ('title','body','caption','check','notes'):
   if isinstance(s.get(k),str):s[k]=correct(s[k],filename)
  if signature(s)!=a['signature']:raise ValueError(f'Review lecturer notes after content change: {filename} slide {i}')
  s['notes']=a['notes']
