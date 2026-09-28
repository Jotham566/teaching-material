import json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from calibration_record import complete,model_for_report,profile_for_report
class CalibrationModelChecks(unittest.TestCase):
 def report(self,folder,models,passed=True):
  p=Path(folder)/'report.json';rows=[dict(case=str(i),passed=passed,result=dict(model=m)) for i,m in enumerate(models)]
  p.write_text(json.dumps(rows));complete(p,[r['case'] for r in rows]);return p
 def test_uses_recorded_local_model(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.report(d,['qwen3.5:4b']*5);self.assertEqual(model_for_report(p),'qwen3.5:4b')
 def test_failed_mixed_and_cloud_reports_cannot_select_model(self):
  with tempfile.TemporaryDirectory() as d:
   for models,passed in [(['qwen3:4b']*5,False),(['qwen3:4b']*4+['qwen3.5:4b'],True),(['qwen3:cloud']*5,True)]:
    p=self.report(d,models,passed)
    with self.assertRaises(ValueError):model_for_report(p)
 def test_stale_report_cannot_select_model(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.report(d,['qwen3:4b']*5);p.write_text(p.read_text()+' ')
   with self.assertRaises(ValueError):model_for_report(p)

 def test_profile_is_consistent_and_supported(self):
  with tempfile.TemporaryDirectory() as d:
   p=self.report(d,['qwen3.5:4b']*5);self.assertEqual(profile_for_report(p),'standard')
   rows=json.loads(p.read_text())
   for r in rows:r['result']['evaluation_profile']='reasoned'
   p.write_text(json.dumps(rows));complete(p,[r['case'] for r in rows]);self.assertEqual(profile_for_report(p),'reasoned')
   rows[0]['result']['evaluation_profile']='unknown';p.write_text(json.dumps(rows));complete(p,[r['case'] for r in rows])
   with self.assertRaises(ValueError):profile_for_report(p)
