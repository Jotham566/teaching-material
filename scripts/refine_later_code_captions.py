"""Keep explanations and output captions attached to the matching code part."""
import json,re
from pathlib import Path
from descriptive_teaching_names import MEANINGS
ROOT=Path(__file__).resolve().parents[1]
MEANINGS.update(X_train='input columns used for training',y_train='observed targets for the training rows',X_valid='input columns used for validation',y_valid='observed targets used to check predictions',mae='mean absolute error',rmse='root mean squared error')
def apply():
 p=ROOT/'data/iuea_deck_content.json';ds=json.loads(p.read_text())
 for d in ds:
  if d['week']<8:continue
  group=[]
  def finish(group):
   if not group:return
   caption=group[0].get('complete_example_caption', group[-1].get('caption','') if len(group)>1 and group[0].get('caption','').startswith('Continue in the same code cell.') else group[0].get('caption',''))
   for j,s in enumerate(group):
    s['complete_example_caption']=caption
    names=re.findall(r'^([A-Za-z_][A-Za-z_0-9]*)\s*=',s['code'],re.M)
    known=[n for n in names if n in MEANINGS]
    if known:s['explain']=[known[0]+': '+MEANINGS[known[0]]+'.']
    else:s['explain']=['Continue the indented statement from the previous part.' if s['code'].startswith(' ') else 'Use the inputs and operations defined in the preceding slides.']
    if len(group)>1:s['caption']=caption if j==len(group)-1 else 'Continue in the same code cell. The result appears after the final part.'
  for s in d['slides']:
   if s.get('code'):
    if s.get('practice_code'):finish(group);group=[]
    group.append(s)
   else:finish(group);group=[]
  finish(group)
 p.write_text(json.dumps(ds,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':apply()
