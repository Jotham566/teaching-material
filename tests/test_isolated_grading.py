import json,os,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'IUEA_Teaching_Plan/grader'
sys.path.insert(0,str(HERE))
from batch_grade import grade_one
from isolated_grading import preflight
class IsolationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):preflight()
 def run_notebook(self,source,timeout=4):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'S99997_W03.ipynb'
   p.write_text(json.dumps({'cells':[{'cell_type':'code','metadata':{},'source':source}]}))
   return grade_one(str(p),str(HERE/'specs/spec_W03.py'),str(HERE/'specs/hidden/spec_W03_hidden.py'),'W03','CML3111',None,1,timeout,None)
 def test_correct_functions(self):
  r=self.run_notebook('''weight_n=40*9.81
def percent_error(measured,expected):return 100*(measured-expected)/expected
def power_loss(i,r):return i*i*r
def efficiency(out_w,in_w):return None if in_w<=0 else 100*out_w/in_w
worst_reading=111.4
worst_error=11.4''')
  self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),20,r)
 def test_checker_replacement(self):
  r=self.run_notebook('import iuea_grader as ig\nig.run_check=lambda *a: ig.Result("q1",True,20,20,"forged")')
  self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),0,r)
 def test_host_file_is_not_visible(self):
  with tempfile.TemporaryDirectory() as tmp:
   sentinel=Path(tmp)/'sentinel.txt';sentinel.write_text('teaching-isolation-test')
   r=self.run_notebook('weight_n = 392.4 if __import__("pathlib").Path('+repr(str(sentinel))+').exists() else 0')
   self.assertEqual(r['questions']['q1']['awarded'],0)
 def test_hard_timeout(self):
  r=self.run_notebook('import signal\nsignal.alarm(0)\nwhile True: pass',timeout=2)
  self.assertEqual(r['status'],'TIMEOUT',r)
 def test_week2_fixture_scores_fourteen(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'99_TEST_000_DEMO-X_W02.ipynb'
   folder=ROOT/'IUEA_Teaching_Plan/setup/CML3112'
   p.write_text((folder/'proof_of_life.ipynb').read_text().replace('YOUR_ID','99/TEST/000/DEMO-X'))
   r=grade_one(str(p),str(HERE/'specs/spec_W02.py'),str(HERE/'specs/hidden/spec_W02_hidden.py'),'W02','CML3112',str(folder),2,10,None)
   self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),14,r)
   self.assertEqual(r['student_id'],'99/TEST/000/DEMO-X')
   self.assertNotEqual(r['status'],'IDENTITY_MISMATCH')
 def test_freeform_week2_registration_scores_fourteen(self):
  from registration import filename_id
  sid='99/0000/DEMO-X'
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/(filename_id(sid)+'_W02.ipynb')
   folder=ROOT/'IUEA_Teaching_Plan/setup/CML3112'
   p.write_text((folder/'proof_of_life.ipynb').read_text().replace('YOUR_ID',sid))
   r=grade_one(str(p),str(HERE/'specs/spec_W02.py'),str(HERE/'specs/hidden/spec_W02_hidden.py'),'W02','CML3112',str(folder),2,10,None)
   self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),14,r)
   self.assertEqual(r['student_id'],sid)
   self.assertNotEqual(r['status'],'IDENTITY_MISMATCH')
 def test_week4_correct_results(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'S99997_W04.ipynb'
   source='''STUDENT_ID="S99997"
COHORT="CML3111"
import csv
with open('motor_test_bench.csv') as f:rows=list(csv.DictReader(f))
valid=[r for r in rows if r['winding_temp_c']!='']
valid_count=len(valid)
mean_reading=sum(float(r['winding_temp_c']) for r in valid)/valid_count
above_limit=sum(float(r['winding_temp_c'])>130 for r in valid)
group_means={g:sum(float(r['winding_temp_c']) for r in valid if r['motor_id']==g)/sum(r['motor_id']==g for r in valid) for g in {r['motor_id'] for r in valid}}
'''
   p.write_text(json.dumps({'cells':[{'cell_type':'code','metadata':{},'source':source}]}))
   r=grade_one(str(p),str(HERE/'specs/spec_W04.py'),str(HERE/'specs/hidden/spec_W04_hidden.py'),'W04','CML3111',str(ROOT/'IUEA_Teaching_Plan/practicals/W04/CML3111'),2,10,None)
   self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),20,r)
 def test_colab_absolute_paths_share_the_isolated_working_directory(self):
  r=self.run_notebook('''from pathlib import Path
Path("local.txt").write_text("same folder")
assert Path("/content/local.txt").read_text()=="same folder"
Path("/content/colab.txt").write_text("round trip")
assert Path("colab.txt").read_text()=="round trip"
weight_n=40*9.81
''',timeout=10)
  self.assertFalse(r['cell_errors'],r)
  self.assertEqual(r['questions']['q1']['awarded'],r['questions']['q1']['marks'])
 def test_colab_upload_only_returns_supplied_csv(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'S99997_W03.ipynb'
   p.write_text(json.dumps({'cells':[{'cell_type':'code','source':'''from google.colab import files
uploaded=files.upload()
assert sorted(uploaded)==["campus_energy.csv"]
assert uploaded["campus_energy.csv"]==open("/content/campus_energy.csv","rb").read()
weight_n=40*9.81
'''}]}))
   r=grade_one(str(p),str(HERE/'specs/spec_W03.py'),str(HERE/'specs/hidden/spec_W03_hidden.py'),
               'W03','CML3111',str(ROOT/'IUEA_Teaching_Plan/practicals/W05/CML3111'),2,10,None)
   self.assertFalse(r['cell_errors'],r)
   self.assertEqual(r['questions']['q1']['awarded'],r['questions']['q1']['marks'])
if __name__=='__main__':unittest.main()
