"""Regression checks for the beginner notebook workflow and legacy marking."""
import copy,json,os,re,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from batch_grade import grade_one
from test1_coding_reference import complete_notebook,NOTEBOOK_ANSWERS
from test1_coding_contracts import PARTS
class CodingTests(unittest.TestCase):
 def notebook(self):return json.loads((G.parent/'assessment_banks/TEST1/CML3111/A/TEST1_student.ipynb').read_text())
 def grade(self,nb,variant='A'):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'test.ipynb';path.write_text(json.dumps(nb))
   return grade_one(str(path),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1','CML3111',str(G.parent/'assessment_banks/TEST1/CML3111'/variant),20,180,None)
 def score(self,result):return sum(q['awarded'] for q in result['questions'].values())
 def replace(self,nb,task,source):
  for c in nb['cells']:
   if 'iuea-answer-'+task in c.get('metadata',{}).get('tags',[]):c['source']=source
 def test_structure(self):
  nb=self.notebook();code=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code' and 'autograde-skip' not in c.get('metadata',{}).get('tags',[])]
  self.assertEqual(sum('def ' in s for s in code),1)
  self.assertEqual(sum(m for _,m in PARTS),100)
  self.assertNotIn('pathlib','\n'.join(code))
  self.assertIn('Student ID/ Registration Number',''.join(nb['cells'][0]['source']))
  self.assertIn('Do not edit this cell',''.join(nb['cells'][3]['source']))
  self.assertIn('## Start here',''.join(nb['cells'][0]['source']))
  self.assertIn('submit only once',''.join(nb['cells'][0]['source']))
  self.assertIn('Click **Connect**',''.join(nb['cells'][0]['source']))
  final_guide=''.join(nb['cells'][-2]['source'])
  self.assertIn('## Need help with a technical problem?',final_guide)
  self.assertIn('## Save and submit',final_guide)
  self.assertIn('One submission only',final_guide)
  self.assertIn('Your response has been recorded',final_guide)
 def test_isna_and_isnull_are_both_accepted(self):
  nb=complete_notebook(self.notebook())
  self.replace(nb,'eda',NOTEBOOK_ANSWERS['eda'].replace('.isnull()', '.isna()'))
  result=self.grade(nb);self.assertEqual(self.score(result),100,result)
 def test_partial_statistics(self):
  nb=complete_notebook(self.notebook());self.replace(nb,'statistics',NOTEBOOK_ANSWERS['statistics']+'\ntarget_std = 0\n')
  r=self.grade(nb);self.assertEqual(self.score(r),97.5,r)
 def test_required_info_and_tail(self):
  nb=complete_notebook(self.notebook());self.replace(nb,'eda',NOTEBOOK_ANSWERS['eda'].replace('raw_data.info()','').replace('last_rows = raw_data.tail()','last_rows = raw_data.head()'))
  r=self.grade(nb);self.assertEqual(self.score(r),97,r)
 def test_function_uses_inputs(self):
  nb=complete_notebook(self.notebook());self.replace(nb,'function',"def calculate_column_statistics(table,column_name):\n    return {'mean':target_mean,'sum':target_sum,'median':target_median}\n")
  r=self.grade(nb);self.assertEqual(self.score(r),95,r)
 def test_loop_cannot_be_replaced_with_counts(self):
  nb=complete_notebook(self.notebook());self.replace(nb,'loops',NOTEBOOK_ANSWERS['loops'].replace('for load in cleaned_data', 'for load in cleaned_data'))
  # Correct results without the requested loop/conditions earn only the result marks.
  self.replace(nb,'loops',"load_band_counts = {'low':int((cleaned_data.load_pct<40).sum()),'medium':int(cleaned_data.load_pct.between(40,75).sum()),'high':int((cleaned_data.load_pct>75).sum())}\n")
  r=self.grade(nb);self.assertEqual(self.score(r),96,r)
 def test_old_issued_v3_notebook_still_scores_100(self):
  rel='IUEA_Teaching_Plan/assessment_banks/TEST1/CML3111/A/TEST1_student.ipynb'
  nb=json.loads(subprocess.check_output(['git','show','26f271ea:'+rel],cwd=ROOT))
  source=(G/'test1_coding_reference.py').read_text().split('# Lecturer-only answers')[0]
  for c in nb['cells']:
   text=''.join(c['source'])
   if c['cell_type']=='code' and text.startswith('def '):c['source']=source
   if 'iuea-read-csv' in c.get('metadata',{}).get('tags',[]):c['source']='file_path="engineering_data.csv"\nraw_data=pd.read_csv(file_path)\n'
  r=self.grade(nb);self.assertEqual(self.score(r),100,r)
 def test_actual_portal_notebook(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'portal.ipynb'
   subprocess.run(['node','tests/test_timed_takehome.cjs'],cwd=ROOT,env={**os.environ,'IUEA_TEST_PACKET_OUT':str(path)},check=True,capture_output=True)
   nb=json.loads(path.read_text());variant=re.search(r'VARIANT = "([ABC])"',''.join(nb['cells'][-1]['source']))[1]
   self.assertNotIn('pd.read_csv',''.join(nb['cells'][3]['source']))
   r=self.grade(complete_notebook(nb),variant)
   self.assertEqual(r['declared_sid'],'DEMO / TIMED',r);self.assertEqual(self.score(r),100,r)
 def test_colab_snapshot_without_custom_cell_tags(self):
  with tempfile.TemporaryDirectory() as temp:
   path=Path(temp)/'portal.ipynb'
   subprocess.run(['node','tests/test_timed_takehome.cjs'],cwd=ROOT,env={**os.environ,'IUEA_TEST_PACKET_OUT':str(path)},check=True,capture_output=True)
   nb=complete_notebook(json.loads(path.read_text()))
   variant=re.search(r'VARIANT = "([ABC])"',''.join(nb['cells'][-1]['source']))[1]
   for cell in nb['cells']:cell.get('metadata',{}).pop('tags',None)
   r=self.grade(nb,variant)
   self.assertEqual(r['declared_sid'],'DEMO / TIMED',r)
   self.assertEqual(self.score(r),100,r)
   self.assertEqual(r['cell_errors'],[],r)
   # Ordinary answer errors must still be reported.
   nb['cells'].append({'cell_type':'code','metadata':{},'source':'raise ValueError("student answer error")','outputs':[],'execution_count':None})
   r=self.grade(nb,variant)
   self.assertEqual(len(r['cell_errors']),1,r)
   self.assertEqual(r['cell_errors'][0]['etype'],'ValueError',r)
if __name__=='__main__':unittest.main()
