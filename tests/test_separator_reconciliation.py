import copy
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import continuous_assessment as ca
from reconcile_registrations import reconcile
from test_registration_reconciliation import row
import tempfile

class SeparatorTests(unittest.TestCase):
 def run_rows(self,rows):
  with tempfile.TemporaryDirectory() as tmp:
   ledger=ca.finalize(copy.deepcopy(rows),[])
   return reconcile(ledger,{},Path(tmp),separator_only=True)
 def test_known_separator_variants_release_same_account_marks(self):
  for bad,target in [('99-987-BSPE-S','99/987/BSPE-S'),('99UG987BSPE-S','99/UG/987/BSPE-S'),('99987/BSPE-S','99/987/BSPE-S'),('99/987/BSPES','99/987/BSPE-S')]:
   d=self.run_rows([row(bad),row(target,'r2',assessment='Q2'),row(target,'r3',assessment='Q3')])
   self.assertEqual({r['student_id'] for r in d['attempts']},{target})
   self.assertTrue(all(r['score']==4 for r in d['current']))
 def test_digit_and_suffix_conflicts_remain_held(self):
  for bad in ('98/987/BSPE-S','99/988/BSPE-S','99/987/BSPE-J','99/987/BSP-S'):
   d=self.run_rows([row(bad),row('99/987/BSPE-S','r2',assessment='Q2'),row('99/987/BSPE-S','r3',assessment='Q3')])
   self.assertEqual(d['attempts'][0]['student_id'],bad)
   self.assertTrue(all(r['score'] is None for r in d['current']))
 def test_unknown_boundaries_not_guessed(self):
  d=self.run_rows([row('99987/BSPE-S'),row('99/987/BSPE-S','r2',assessment='Q2'),row('999/87/BSPE-S','r3',assessment='Q3')])
  self.assertEqual(d['attempts'][0]['student_id'],'99987/BSPE-S')
 def test_target_on_another_account_alone_not_enough(self):
  d=self.run_rows([row('99-987-BSPE-S'),row('99/987/BSPE-S','r2',email='other@example.test',assessment='Q2'),row('99/987/BSPE-S','r3',email='other@example.test',assessment='Q3')])
  self.assertEqual(d['attempts'][0]['student_id'],'99/987/BSPE-S')
  self.assertTrue(all(r['score'] is None for r in d['current']))
 def test_formatting_does_not_release_other_account_conflicts(self):
  d=self.run_rows([row('99-987-BSPE-S'),row('99/987/BSPE-S','r2',assessment='Q2'),row('99/987/BSPE-S','r3',email='other@example.test',assessment='Q3')])
  self.assertEqual(len(d['students']),1)
  self.assertTrue(all(r['score'] is None for r in d['current']))

if __name__=='__main__':unittest.main()
