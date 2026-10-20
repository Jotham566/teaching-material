"""Execute the ungraded Week 6 beginner walkthrough with the issued CSV."""
import contextlib,io,json,os,shutil,tempfile,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'IUEA_Teaching_Plan'
class BeginnerFiltering(unittest.TestCase):
 def test_workflow_and_package(self):
  for cohort in ('CML3111','CML3112','CML3113'):
   with self.subTest(cohort=cohort):self.check_cohort(cohort)
 def check_cohort(self,cohort):
  path=BASE/f'guided_practice/{cohort}/W06/guided_practice.ipynb';nb=json.loads(path.read_text())
  if cohort!='CML3111':self.assertIn('A6 and Quiz 6 are waived',''.join(nb['cells'][0]['source']))
  else:self.assertNotIn('waived',''.join(nb['cells'][0]['source']))
  d=next(d for d in json.loads((ROOT/'data/iuea_deck_content.json').read_text()) if d['cohort']==cohort and d['week']==6)
  self.assertEqual([''.join(c['source']).strip() for c in nb['cells'] if c['cell_type']=='code'],[s['practice_code'] for s in d['slides'] if s.get('practice_code')])
  original=Path.cwd()
  with tempfile.TemporaryDirectory() as tmp:
   shutil.copy(BASE/f'assessment_banks/W06/{cohort}/A/engineering_data.csv',tmp);os.chdir(tmp);ns={}
   try:
    for c in nb['cells']:
     if c['cell_type']=='code':
      with contextlib.redirect_stdout(io.StringIO()):exec(''.join(c['source']),ns)
    self.assertEqual(len(ns['raw_data']),91);self.assertEqual(len(ns['cleaned_data']),88)
    self.assertEqual(len(ns['rows_with_target']),89)
    self.assertEqual(ns['target_is_recorded'].sum(),89)
    self.assertEqual(ns['load_is_valid'].sum(),89)
    self.assertEqual(ns['rows_to_keep'].sum(),88)
    self.assertFalse(ns['target_is_recorded'].loc[3])
    self.assertFalse(ns['load_is_valid'].loc[8])
    retained=ns['raw_data'].drop_duplicates('record_id')
    retained=retained[retained['target'].notna() & retained['load_pct'].between(0,100)]
    self.assertAlmostEqual(ns['median_ambient_c'],retained['ambient_c'].median())
    self.assertEqual(ns['raw_data']['target'].isna().sum(),1)
    self.assertEqual(ns['cleaned_data'].isna().sum().sum(),0)
   finally:os.chdir(original)
  with zipfile.ZipFile(BASE/f'student_packages/{cohort}_W06_student.zip') as z:
   self.assertEqual(z.read('guided_practice.ipynb'),path.read_bytes())
   self.assertFalse(any('grader' in n.lower() for n in z.namelist()))
if __name__=='__main__':unittest.main()
