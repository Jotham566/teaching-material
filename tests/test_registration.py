import sys,unittest,tempfile,json,csv,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GRADER=ROOT/'IUEA_Teaching_Plan/grader'
sys.path.insert(0,str(GRADER))
from registration import valid,filename_id
from batch_grade import student_id_from_name
from artifact_grade import group_manifest
class RegistrationTests(unittest.TestCase):
 def test_round_trip(self):
  sid='99/TEST/000/DEMO-X'
  self.assertTrue(valid(sid))
  self.assertEqual(filename_id(sid),'99_TEST_000_DEMO-X')
  self.assertEqual(student_id_from_name(filename_id(sid)+'_W02.ipynb'),sid)
  self.assertTrue(valid('S24001'))
  for sid in ('99/0000/DEMO-X','DEMO 007','DEMO_A/B','../../escape','école-démo'):
   with self.subTest(sid=sid):
    self.assertTrue(valid(sid))
    token=filename_id(sid)
    self.assertNotIn('/',token)
    self.assertNotIn('\\',token)
    self.assertEqual(student_id_from_name(token+'_W02.ipynb'),sid.upper())
  for empty in ('','  ',None,'bad\x00id','bad\nid'):
   self.assertFalse(valid(empty))
 def test_artifact_manifest_registration(self):
  sid='99/TEST/000/DEMO-X'
  self.assertIn(sid,group_manifest([dict(student_id=sid,file='report.docx')]))
  with self.assertRaises(ValueError):group_manifest([dict(student_id='',file='report.docx')])
 def test_real_registration_preparation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'downloads').mkdir();(p/'downloads/file1.ipynb').write_text('{}')
   sid='99/0000/DEMO-X'
   for name,rows in [('roster',[dict(student_id=sid,email='student@example.test',cohort='CML3112')]),('audit',[dict(assessment_key='CML3112|W02',student_id=sid,email='student@example.test',status='ON_TIME',submitted_at='2026-09-20T12:00:00Z',deadline='2026-09-22T08:00:00Z',file_ids='["file1"]',response_id='r1',team_id='')])]:
    with (p/(name+'.csv')).open('w') as f:
     w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
   subprocess.run([sys.executable,str(GRADER/'prepare_submissions.py'),'--audit',str(p/'audit.csv'),'--roster',str(p/'roster.csv'),'--assessment','CML3112|W02','--downloads',str(p/'downloads'),'--out',str(p/'out')],check=True,capture_output=True)
   self.assertTrue((p/'out'/(filename_id(sid)+'_W02.ipynb')).exists())
   with (p/'out/manifest.csv').open() as f:
    self.assertEqual(list(csv.DictReader(f))[0]['student_id'],sid)
if __name__=='__main__':unittest.main()
