"""Generate copy-ready prompts and source-scoped inputs from maintained sources."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
DEFAULT=HERE.parents[2]
def make(out,root=DEFAULT):
 out=Path(out);root=Path(root);out.mkdir(parents=True,exist_ok=True)
 data=json.loads((HERE/'demonstrations.json').read_text())
 for s in data:
  for p in s['prompts']:(out/(p['id']+'.txt')).write_text(p['text']+'\n')
 P=root/'03 Learner Materials/Practice Files'
 text=(P/'01 Matter and Sources/Agreement - Executed v2.txt').read_text()
 (out/'Session 03 Standard Terms Only.txt').write_text('STANDARD TERMS ONLY | Key Terms and Order Form deliberately omitted for the source-scope experiment. This file cannot establish the complete executed agreement.\n\n'+text[text.index('SECTION 1.'):])
 cs=json.loads((P/'02 Data and Retrieval/Clause Record.json').read_text());chosen=[x for x in cs if x['clause'] in ('12.6','KT-1')]
 (out/'Session 03 Focused Consent Extract.txt').write_text('FOCUSED CONSENT EXTRACT | Fictional CONTRACT-01 v2. Surrounding contract and transaction evidence are omitted.\n\n'+'\n\n'.join(x['clause']+' | '+x['source_location']+'\n'+x['text'] for x in chosen)+'\n')
 print('Generated',sum(len(x['prompts']) for x in data),'prompts and two evidence-scope files in',out)
if __name__=='__main__':make(*sys.argv[1:3])
