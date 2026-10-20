"""Run the slide-taught functions against the real hidden checks in Docker."""
import ast,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from batch_grade import grade_one
from colab_exam_contracts import decision_keys
class AlignmentTests(unittest.TestCase):
 def test_taught_functions_on_unseen_inputs(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  for d in decks:
   if d['week']!=7:continue
   definitions=[]
   for slide in d['slides']:
    if slide.get('revision_example'):
     definitions += [ast.unparse(n) for n in ast.parse(slide['code']).body if isinstance(n,ast.FunctionDef)]
   source='\n\n'.join(definitions)
   for before,after in [('reading','record_id'),('machine','equipment_id'),('load','load_pct'),('ambient','ambient_c')]:
    source=source.replace(repr(before),repr(after))
   source+='\nclean_records = revision_clean\nsummarize_records = revision_summary\nbuild_charts = revision_charts\nfive_findings = revision_findings\n'
   source='import pandas as pd\nimport matplotlib.pyplot as plt\nSTUDENT_ID="DEMO-ALIGNMENT"\nCOHORT='+repr(d['cohort'])+'\n'+source+'\nDECISIONS='+repr(decision_keys()['TEST1'])
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'DEMO-ALIGNMENT_TEST1.ipynb';p.write_text(json.dumps({'cells':[{'cell_type':'code','source':source}]}))
    r=grade_one(str(p),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1',d['cohort'],None,20,120,None)
    self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),100,(d['cohort'],r))
    print(d['cohort'],'slide-taught functions passed hidden checks',flush=True)
if __name__=='__main__':unittest.main()
