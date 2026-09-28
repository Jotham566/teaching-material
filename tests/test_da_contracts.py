import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import da_reference as reference
from da_contracts import TASKS,check
class DAContracts(unittest.TestCase):
 def test_references_and_wrong_constants(self):
  class NS:
   def get(self,name):return getattr(reference,name)
  class Wrong:
   def get(self,name):return lambda *args: {}
  for task in TASKS:
   self.assertTrue(check(NS(),task)[0],task);self.assertFalse(check(Wrong(),task)[0],task)
 def test_reference_notebook_in_isolation(self):
  from batch_grade import grade_one
  with tempfile.TemporaryDirectory() as d:
   file=Path(d)/'S10001_S09.ipynb';file.write_text(json.dumps(dict(cells=[dict(cell_type='code',source='STUDENT_ID="S10001"\nCOHORT="DA"\n'+Path(reference.__file__).read_text())])))
   result=grade_one(str(file),str(G/'specs/spec_S09.py'),str(G/'specs/hidden/spec_S09_hidden.py'),'S09','DA',None,10,40,None)
   self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),50,result)
 def test_inplace_cleaning_is_rejected(self):
  from batch_grade import grade_one
  source=Path(reference.__file__).read_text()+'\n_original=normalise_orders\ndef normalise_orders(rows,aliases):\n result=_original(rows,aliases)\n rows.clear()\n return result\n'
  with tempfile.TemporaryDirectory() as d:
   file=Path(d)/'S10001_S09.ipynb';file.write_text(json.dumps(dict(cells=[dict(cell_type='code',source='STUDENT_ID="S10001"\nCOHORT="DA"\n'+source)])))
   result=grade_one(str(file),str(G/'specs/spec_S09.py'),str(G/'specs/hidden/spec_S09_hidden.py'),'S09','DA',None,10,40,None)
   self.assertEqual(result['questions']['q1']['awarded'],0,result)
if __name__=='__main__':unittest.main()
