import copy, hashlib, json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'IUEA_Teaching_Plan/grader'))
import exam_intake as intake
class IntakeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.folder=Path(self.tmp.name);self.path=self.folder/'test.ipynb';self.path.write_text('{"nbformat":4,"cells":[]}')
  self.db=intake.connect(self.folder/'ledger.db')
  self.job=dict(response_id='response-1',cohort='CML3111',assessment='TEST1',variant='A',full_name='Synthetic Learner',email='test@example.com',email_verified=True,student_registration_number='DEMO / free form',submitted_at='2026-10-19T09:30:00+03:00',opens_at='2026-10-19T09:00:00+03:00',closes_at='2026-10-19T12:00:00+03:00',notebook_sha256=hashlib.sha256(self.path.read_bytes()).hexdigest())
  self.result=dict(status='OK',declared_sid='DEMO / free form',questions={'q1':{'awarded':80}},cell_errors=[])
 def tearDown(self):self.db.close();self.tmp.cleanup()
 def process(self,job=None,result=None):
  with patch.object(intake,'grade_one',return_value=result or self.result) as grader:
   return intake.process(job or self.job,self.path,self.db),grader.call_count
 def test_grading_and_duplicate(self):
  r,n=self.process();self.assertEqual((r['status'],r['score'],r['semester_points']),('GRADED',80,12))
  r,n=self.process();self.assertEqual(n,0);self.assertEqual(len(intake.records(self.db)),1)
 def test_current_test1_dispatch_ignores_old_private_snapshot(self):
  def check_dispatch(*args):
   text=Path(args[2]).read_text()
   self.assertIn('test1_coding_contracts',text)
   self.assertIn("'q8'",text)
   self.assertNotIn('decisions',text)
   return self.result
  with patch.object(intake,'grade_one',side_effect=check_dispatch):
   result=intake.process(self.job,self.path,self.db)
  self.assertEqual(result['grader_version'],'2026.10-test1-coding-v3')
 def test_late_has_no_mark(self):
  self.job['submitted_at']='2026-10-19T12:00:01+03:00';r,n=self.process();self.assertEqual(r['status'],'OUTSIDE_WINDOW');self.assertIsNone(r['score']);self.assertEqual(n,0)
 def test_identity_conflict_withholds_both(self):
  self.process();job=dict(self.job,response_id='response-2',email='other@example.com');r,n=self.process(job);self.assertEqual(n,0)
  self.assertTrue(all(x['status']=='IDENTITY_CONFLICT' and x['score'] is None for x in intake.records(self.db)))
 def test_unverified_rejected(self):
  self.job['email_verified']=False
  with self.assertRaisesRegex(ValueError,'verified'):self.process()
 def test_infrastructure_failure_stays_pending(self):
  r,n=self.process(result=dict(self.result,status='HARNESS_ERROR',declared_sid=''));self.assertEqual(r['status'],'HARNESS_ERROR');self.assertIsNone(r['score'])
 def test_notebook_identity_mismatch(self):
  r,n=self.process(result=dict(self.result,declared_sid='ANOTHER'));self.assertEqual(r['status'],'IDENTITY_MISMATCH');self.assertIsNone(r['score'])
 def test_duplicate_receipt_metadata_cannot_change(self):
  self.process();self.job['assessment']='TEST2'
  with self.assertRaisesRegex(ValueError,'metadata'):self.process()
 def test_latest_pending_does_not_silently_release_old_mark(self):
  self.process();job=dict(self.job,response_id='response-2',submitted_at='2026-10-19T10:30:00+03:00');self.process(job,dict(self.result,status='TIMEOUT'))
  latest=intake.current(intake.records(self.db));self.assertEqual(latest[0]['status'],'TIMEOUT');self.assertIsNone(latest[0]['score'])
 def test_formula_text_escaped_in_csv(self):
  self.job['full_name']='=1+1';self.process();intake.export(self.db,self.folder);self.assertIn("'=1+1",(self.folder/'current_marks.csv').read_text())
if __name__=='__main__':unittest.main()
