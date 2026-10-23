"""Regression checks for partial credit, boundary values and authentic plots."""
import ast,inspect,json,sys,tempfile,unittest,subprocess,os,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import test1_coding_contracts as contract
import test1_coding_reference as reference
from isolated_grading import decode
from batch_grade import grade_one
class NS:
 def __init__(self, **overrides):self.overrides=overrides
 def get(self,name,default=None):
  import pandas as pd
  if name in ('raw_data','_IUEA_ASSIGNED_DATA'):return self.overrides.get(name,pd.DataFrame(contract.dataset('CML3112',17,dirty=True)))
  return self.overrides.get(name,'CML3112' if name=='COHORT' else getattr(reference,name,default))
 def has_syntax(self,name,kind):return True
class CodingTests(unittest.TestCase):
 def test_nonplot_full_credit_and_boundaries(self):
  for course in ('CML3111','CML3112','CML3113'):
   for task in ('eda','cleaning','statistics','grouping','conditions','loops'):
    self.assertEqual(contract.assess(NS(COHORT=course),task)[2],1,(course,task))
 def test_statistic_partial_credit(self):
  def wrong_std(rows):
   out=reference.calculate_statistics(rows);out['std']=0;return out
  self.assertAlmostEqual(contract.assess(NS(calculate_statistics=wrong_std),'statistics')[2],5/6)
 def test_one_wrong_group_column(self):
  def wrong_sum(rows):
   out=reference.summarize_equipment(rows);out['sum']=0;return out
  self.assertAlmostEqual(contract.assess(NS(summarize_equipment=wrong_sum),'grouping')[2],2/3)
 def test_forged_figure_rejected(self):
  self.assertEqual(contract.assess(NS(plot_observations=lambda *args:{'plot_axes':[]}), 'before')[2],0)
 def test_mode_must_include_every_tie(self):
  self.assertFalse(contract.equal(['E1'],['E1','E2']))
 def test_issued_portal_packet_grades_identity_and_csv_reading(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'portal.ipynb'
   subprocess.run(['node','tests/test_timed_takehome.cjs'],cwd=ROOT,env={**os.environ,'IUEA_TEST_PACKET_OUT':str(path)},check=True,capture_output=True)
   nb=json.loads(path.read_text())
   self.assertNotIn('pathlib',''.join(nb['cells'][3]['source']))
   self.assertNotIn('pd.read_csv',''.join(nb['cells'][3]['source']))
   variant=re.search(r'VARIANT = "([ABC])"',''.join(nb['cells'][-1]['source']))[1]
   for c in nb['cells']:
    source=''.join(c['source'])
    if c['cell_type']=='code' and source.startswith('def '):c['source']=(G/'test1_coding_reference.py').read_text()
    if 'iuea-read-csv' in c.get('metadata',{}).get('tags',[]):c['source']='file_path = "engineering_data.csv"\nraw_data = pd.read_csv(file_path)\n'
   path.write_text(json.dumps(nb))
   result=grade_one(str(path),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1','CML3111',str(G.parent/'assessment_banks/TEST1/CML3111'/variant),20,180,None)
   self.assertEqual(result['declared_sid'],'DEMO / TIMED',result)
   self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),100,result)
 def test_csv_reading_has_two_marks(self):
  self.assertAlmostEqual(contract.assess(NS(raw_data=None),'eda')[2],.8)
 def test_cleaning_failure_does_not_zero_other_tasks(self):
  folder=G.parent/'assessment_banks/TEST1/CML3111/A'
  nb=json.loads((folder/'TEST1_student.ipynb').read_text())
  source=(G/'test1_coding_reference.py').read_text()
  for c in nb['cells']:
   text=''.join(c['source'])
   if 'iuea-read-csv' in c.get('metadata',{}).get('tags',[]):c['source']='file_path = "engineering_data.csv"\nraw_data = pd.read_csv(file_path)\n'
   if c['cell_type']=='code' and text.startswith('def '):
    c['source']=source+'\ndef clean_observations(input_records):\n    raise ValueError("unfinished")\n'
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'partial.ipynb';p.write_text(json.dumps(nb))
   result=grade_one(str(p),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1','CML3111',str(folder),20,180,None)
  self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),80,result)
if __name__=='__main__':unittest.main()
