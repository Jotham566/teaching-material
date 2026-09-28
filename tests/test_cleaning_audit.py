import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from engineering_reference import audit_cleaning
from engineering_contracts import check
class CleaningAudit(unittest.TestCase):
 def test_counts_measure_actual_defects(self):
  raw=[{'record_id':1,'target':3,'load_pct':50}]*4
  cleaned=[dict(raw[0]),dict(raw[0]),{'record_id':2,'target':None,'load_pct':-1}]
  self.assertEqual(audit_cleaning(raw,cleaned),dict(raw_count=4,cleaned_count=3,duplicate_ids=1,missing_targets=1,invalid_loads=1))
 def test_always_clean_claim_does_not_pass(self):
  class NS:
   def get(self,name,default=None):
    if name=='COHORT':return 'CML3111'
    return lambda raw,cleaned:dict(raw_count=len(raw),cleaned_count=len(cleaned),duplicate_ids=0,missing_targets=0,invalid_loads=0)
  self.assertFalse(check(NS(),'audit')[0])
 def test_input_mutation_is_rejected_in_isolation(self):
  from batch_grade import grade_one
  source=(G/'engineering_reference.py').read_text()+'\n_original_audit=audit_cleaning\ndef audit_cleaning(raw,cleaned):\n answer=_original_audit(raw,cleaned)\n raw.clear()\n return answer\n'
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'99_TEST_000_DEMO-X_W06.ipynb';p.write_text(json.dumps({'cells':[{'cell_type':'code','source':'STUDENT_ID="99/TEST/000/DEMO-X"\nCOHORT="CML3111"\n'+source}]}))
   r=grade_one(str(p),str(G/'specs/spec_W06.py'),str(G/'specs/hidden/spec_W06_hidden.py'),'W06','CML3111',None,10,40,None)
   self.assertEqual(r['questions']['q3']['awarded'],0,r)
if __name__=='__main__':unittest.main()
