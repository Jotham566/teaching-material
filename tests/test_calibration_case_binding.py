import copy,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from calibration_record import validate_current_cases,authored_cases

class CurrentCaseChecks(unittest.TestCase):
 def setUp(self):
  self.expected=authored_cases('W08')
  self.rows=[dict(case=n,expected_range=c['expected_range'],result=dict(source_sha256=c['source_sha256'],score=c['expected_range'][0])) for n,c in self.expected.items()]
 def test_complete_current_inputs_pass(self):
  validate_current_cases(self.rows,'W08')
 def test_old_subset_cannot_authorize_new_cases(self):
  with self.assertRaisesRegex(ValueError,'case set'):validate_current_cases(self.rows[:-1],'W08')
 def test_unfinished_assessment_cannot_use_arbitrary_cases(self):
  with self.assertRaisesRegex(ValueError,'No authored'):validate_current_cases(self.rows,'S15')
 def test_altered_text_or_expected_marks_rejected(self):
  for field in ('text','marks','score'):
   rows=copy.deepcopy(self.rows)
   if field=='text':rows[0]['result']['source_sha256']='different'
   elif field=='marks':rows[0]['expected_range']=[0,10]
   else:rows[0]['result']['score']=-1
   with self.subTest(field=field),self.assertRaises(ValueError):validate_current_cases(rows,'W08')
 def test_w02_hash_matches_actual_packet_files(self):
  from calibrate_local_grader import CASES
  from artifact_grade import packet_hash
  name,explanation,readme,lo,hi=CASES[0]
  with tempfile.TemporaryDirectory() as d:
   nb=Path(d)/'answer.ipynb';md=Path(d)/'README.md'
   nb.write_text(json.dumps({'cells':[{'cell_type':'markdown','source':['My explanation: '+explanation]}]}));md.write_text(readme)
   self.assertEqual(authored_cases('W02')[name]['source_sha256'],packet_hash([nb,md]))

if __name__=='__main__':unittest.main()
