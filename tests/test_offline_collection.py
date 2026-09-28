import sys,tempfile,unittest,json,csv
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from collect_offline import collect
class OfflineTests(unittest.TestCase):
 def test_receipt_uses_collection_clock_not_file_time(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'intake';src.mkdir();(src/'99_TEST_000_DEMO-X_TEST1.ipynb').write_text('{}')
   roster=[dict(student_id='99/TEST/000/DEMO-X',cohort='CML3111')]
   receipts=collect(src,roster,'TEST1','CML3111','2026-10-23T14:00:00+03:00',p/'late',datetime(2026,10,23,11,0,1,tzinfo=timezone.utc))
   self.assertEqual(receipts[0]['status'],'LATE')
   with (p/'late/manifest.csv').open() as f:self.assertEqual(list(csv.DictReader(f)),[])
   good=collect(src,roster,'TEST1','CML3111','2026-10-23T14:00:00+03:00',p/'good',datetime(2026,10,23,11,0,0,tzinfo=timezone.utc))
   self.assertEqual(good[0]['status'],'ON_TIME')
   with self.assertRaises(ValueError):collect(src,roster,'TEST1','CML3111','2026-10-23T14:00:00+03:00',p/'good')
 def test_nested_intake_and_duplicate_registration(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'intake';seat=src/'seat01';seat.mkdir(parents=True)
   (seat/'99_TEST_000_DEMO-X_TEST1.IPYNB').write_text('{}')
   roster=[dict(student_id='99/TEST/000/DEMO-X',cohort='CML3111')]
   kwargs=dict(assessment='TEST1',cohort='CML3111',deadline='2026-10-23T14:00:00+03:00',now=datetime(2026,10,23,10,0,tzinfo=timezone.utc))
   self.assertEqual(len(collect(src,roster,out=p/'ok',**kwargs)),1)
   duplicate=src/'seat02';duplicate.mkdir();(duplicate/'99_TEST_000_DEMO-X_TEST1.ipynb').write_text('{}')
   with self.assertRaisesRegex(ValueError,'duplicate'):collect(src,roster,out=p/'duplicate',**kwargs)
   self.assertEqual(list((p/'duplicate').iterdir()),[])
 def test_freeform_roster_number_is_encoded_for_grading(self):
  from registration import registration_from_filename
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);src=p/'intake';src.mkdir()
   (src/'99_0000_DEMO-X_TEST1.ipynb').write_text('{}')
   receipts=collect(src,[dict(student_id='99/0000/DEMO-X',cohort='CML3111')],'TEST1','CML3111','2026-10-23T14:00:00+03:00',p/'out',datetime(2026,10,23,10,0,tzinfo=timezone.utc))
   self.assertEqual(registration_from_filename(receipts[0]['file']),'99/0000/DEMO-X')
   self.assertTrue((p/'out'/receipts[0]['file']).exists())
if __name__=='__main__':unittest.main()
