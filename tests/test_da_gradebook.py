import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from da_gradebook import combine
class IndependentGradebookTests(unittest.TestCase):
 def setUp(self):self.roster=[dict(student_id='S10001',name='Synthetic learner',cohort='DA')]
 def result(self,score=80,status='AUTO_SCORED',sid='S10001'):return [dict(student_id=sid,status=status,score=score,maximum=100)]
 def test_weights_and_missing(self):
  self.assertEqual(combine(self.roster,{'S05':self.result()})[0]['final_percent'],'')
  row=combine(self.roster,{s:self.result(v) for s,v in [('S05',100),('S09',80),('S13',60),('S15',90)]})[0]
  self.assertEqual(row['final_percent'],81)
 def test_failures_are_not_zero_and_zero_is_valid(self):
  row=combine(self.roster,{'S05':self.result(0),'S09':self.result('',status='EXCEPTION')})[0]
  self.assertEqual(row['S05'],0);self.assertEqual(row['S09'],'')
 def test_rejects_mixed_tracks_unknown_ids_and_invalid_marks(self):
  with self.assertRaises(ValueError):combine([dict(student_id='99/TEST/000/DEMO-X',cohort='CML3112')],{})
  for rows in [self.result(sid='S99999'),self.result(float('nan')),self.result(101),self.result()+self.result()]:
   with self.assertRaises(ValueError):combine(self.roster,{'S05':rows})
if __name__=='__main__':unittest.main()
