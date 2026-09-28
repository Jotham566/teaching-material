import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from prepare_grade_import import partition
class GradeImportTests(unittest.TestCase):
 def test_success_and_exception_stay_distinct(self):
  ready,errors=partition([dict(student_id='S12345',score='0',maximum='20',status='AUTO_SCORED'),dict(student_id='S12346',score='',maximum='20',status='EXCEPTION')])
  self.assertEqual(ready[0]['score'],0);self.assertEqual(errors[0]['student_id'],'S12346');self.assertEqual(len(ready),1)
 def test_incomplete_week2_component_rejected(self):
  with self.assertRaises(ValueError):partition([dict(student_id='S12345',notebook_total='14',max_total='14',status='OK')])
 def test_duplicate_rejected(self):
  row=dict(student_id='S12345',score='20',maximum='20',status='OK')
  with self.assertRaises(ValueError):partition([row,row])
