import csv,json,sys,tempfile,unittest
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch,Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import grade_assessment as grading
class WrapperTests(unittest.TestCase):
 def test_manifest_limits_execution_without_blocking_incomplete_packet(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);prepared=root/'prepared';prepared.mkdir();source=prepared/'on_time.ipynb';source.write_text('{}');report=prepared/'report.pdf';report.write_bytes(b'PDF');(prepared/'late.ipynb').write_text('{}')
   with (prepared/'manifest.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=['student_id','file','response_id']);w.writeheader();w.writerows([dict(student_id='99/TEST/000/DEMO-X',file=str(source),response_id='receipt-1'),dict(student_id='24/UG/191/BSME-J',file=str(report),response_id='receipt-2')])
   calls=[]
   def run(command,**kw):
    calls.append(command)
    if command[1].endswith('batch_grade.py'):
     folder=Path(command[command.index('--notebooks')+1]);self.assertEqual([p.name for p in folder.iterdir()],['99_TEST_000_DEMO-X_W03.ipynb'])
     self.assertTrue(command[command.index('--data-dir')+1].endswith('practicals/W03/CML3112'))
     grading.write_csv(Path(command[command.index('--out')+1])/'results.csv',[dict(student_id='99/TEST/000/DEMO-X',status='OK',notebook_total=20,max_total=20)],['student_id','status','notebook_total','max_total'])
   with patch.object(sys,'argv',['grade_assessment','--assessment','W03','--cohort','CML3112','--prepared',str(prepared),'--out',str(root/'out')]),patch.object(grading.subprocess,'run',side_effect=run),patch('artifact_grade.local_model_identity',side_effect=AssertionError('Deterministic work must not call Ollama')):
    grading.main()
   self.assertEqual(len(calls),2)
   with (root/'out/results.csv').open() as f:rows=list(csv.DictReader(f))
   self.assertEqual(rows[0]['score'],'20');self.assertEqual(rows[1]['status'],'EXCEPTION');self.assertEqual(rows[1]['score'],'')
 def test_s09_report_is_required_before_execution(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'a.ipynb';path.write_text('{}')
   valid,invalid=grading.packet_plan({'S10001':[dict(file=str(path))]},'S09')
   self.assertFalse(valid);self.assertIn('S10001',invalid)
 def test_reasoned_calibration_routes_to_its_own_backend(self):
  from calibration_record import complete
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);prepared=root/'prepared';prepared.mkdir()
   files=[prepared/'answer.ipynb',prepared/'README.md']
   for f in files:f.write_text('Synthetic fixture')
   grading.write_csv(prepared/'manifest.csv',[dict(student_id='S10001',file=str(f),response_id='one') for f in files],['student_id','file','response_id'])
   calibration=root/'calibration.json';rows=[dict(case=str(i),passed=True,result=dict(model='qwen3.5:4b',evaluation_profile='reasoned')) for i in range(5)]
   calibration.write_text(json.dumps(rows));complete(calibration,[r['case'] for r in rows]);validator=Mock();calls=[]
   def run(command,**kwargs):
    calls.append(command)
    if Path(command[1]).name=='reasoned_artifact_grade.py':
     self.assertEqual(command[command.index('--model')+1],'qwen3.5:4b')
     grading.write_csv(Path(command[command.index('--out')+1])/'results.csv',[dict(student_id='S10001',status='AUTO_SCORED',score=20,maximum=20)],grading.RESULT_FIELDS)
   args=['grade_assessment','--assessment','W02','--cohort','CML3112','--prepared',str(prepared),'--out',str(root/'out'),'--calibration',str(calibration)]
   with patch.object(sys,'argv',args),patch.object(grading.subprocess,'run',side_effect=run),patch('artifact_grade.local_model_identity',return_value={}),patch('reasoned_artifact_grade.load_backend',return_value=SimpleNamespace(validate_calibration=validator)):
    grading.main()
   validator.assert_called_once();self.assertTrue(any(Path(c[1]).name=='reasoned_artifact_grade.py' for c in calls))
if __name__=='__main__':unittest.main()
