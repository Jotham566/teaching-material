import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from hybrid_result import combine
class HybridGates(unittest.TestCase):
 def setUp(self):
  self.r=dict(maximum=70,criteria=[dict(id='split_reason',parent_criterion='c2',maximum=10),dict(id='other',maximum=60)],execution_gates={'c2':dict(field='q1_marks',equals=10,reason='Published split requirement')})
  self.result=dict(status='AUTO_SCORED',score=70,evaluations=[dict(criteria=[dict(id='split_reason',awarded=10),dict(id='other',awarded=60)]) for _ in range(2)])
  self.d=dict(notebook_total=20,max_total=30,status='OK',q1_marks=0)
 def test_failed_split_cannot_earn_noleakage_prose_marks(self):
  out=combine(self.result,self.r,self.d,30,100);self.assertEqual(out['score'],80);self.assertEqual(out['execution_gate_adjustments'][0]['removed'],10);self.assertEqual(self.result['score'],70)
 def test_pass_and_exception(self):
  self.d.update(q1_marks=10,notebook_total=30);self.assertEqual(combine(self.result,self.r,self.d,30,100)['score'],100)
  self.result.update(status='EXCEPTION',score=None);self.assertIsNone(combine(self.result,self.r,self.d,30,100)['score'])
 def test_missing_gate_evidence_is_not_silently_accepted(self):
  del self.d['q1_marks']
  with self.assertRaises(KeyError):combine(self.result,self.r,self.d,30,100)
if __name__=='__main__':unittest.main()
