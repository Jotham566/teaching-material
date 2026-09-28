import ast,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from assessment_registry import records,CHALLENGE_WEEKS,QUIZ_WEEKS,WEIGHTS
class ContentTests(unittest.TestCase):
 def test_ids_and_weights(self):
  self.assertEqual(sum(WEIGHTS.values()),100)
  for code in ('CML3111','CML3112','CML3113'):
   self.assertEqual([r['week'] for r in records() if r['cohort']==code and r['component']=='challenges'],CHALLENGE_WEEKS)
 def test_sources_parse(self):
  for p in list((ROOT/'scripts').glob('*.py'))+list((ROOT/'IUEA_Teaching_Plan/grader').glob('*.py')):ast.parse(p.read_text())
 def test_quiz_corrections(self):
  from quiz_bank_weeks import BANKS
  text=repr(BANKS[2][3])
  self.assertNotIn('Committing now would save',text)
  self.assertIn('Stage the notebook',text)
  self.assertIn('directly readable',repr(BANKS[12][4]))
 def test_week2_kit_executes(self):
  import os
  for code in ('CML3111','CML3112','CML3113'):
   folder=ROOT/'IUEA_Teaching_Plan/setup'/code
   nb=json.loads((folder/'proof_of_life.ipynb').read_text());ns={};cwd=Path.cwd()
   try:
    os.chdir(folder)
    for cell in nb['cells']:
     if cell['cell_type']=='code':exec(''.join(cell['source']),ns)
    self.assertEqual(ns['readings'],17);self.assertEqual(len(ns['rows']),4)
   finally:os.chdir(cwd)
 def test_published_major_rubrics_match_grader(self):
  from plan_content import RUBRICS
  names={'ML_PROJECT':'Engineering ML Project (25%) - as specified by the lecturer','DA_PROJECT':'Data Analysis Project (10%)','TEST1':'Practical Test 1 - Data Investigation (15%)','TEST2':'Practical Test 2 - End-to-End Engineering ML (20%)','DEMO':'Demo, viva & individual reflection (10%)'}
  for aid,name in names.items():
   actual=json.loads((ROOT/'IUEA_Teaching_Plan/grader/rubrics'/f'{aid}.json').read_text())
   self.assertEqual([(c['title'],c['maximum'],c['description']) for c in actual['criteria']],RUBRICS[name])
if __name__=='__main__':unittest.main()
