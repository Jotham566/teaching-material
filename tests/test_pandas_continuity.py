"""Independent checks that pandas solutions satisfy the existing grading contracts."""
import copy,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader'
sys.path.insert(0,str(G))
import engineering_pandas_reference as pdref
import engineering_reference as original
from engineering_contracts import DOMAINS,TASKS,dataset,same
from batch_grade import grade_one

class PandasContinuity(unittest.TestCase):
 def test_cleaning_order_and_no_input_mutation(self):
  rows=[dict(record_id=1,equipment_id='E1',load_pct=10,ambient_c=20,target=None),
        dict(record_id=1,equipment_id='E1',load_pct=10,ambient_c=20,target=9),
        dict(record_id=2,equipment_id='E1',load_pct=0,ambient_c=None,target=0),
        dict(record_id=3,equipment_id='E2',load_pct=100,ambient_c=24,target=10),
        dict(record_id=4,equipment_id='E2',load_pct=101,ambient_c=99,target=10)]
  before=copy.deepcopy(rows);result=pdref.clean_records(rows)
  self.assertEqual(result,original.clean_records(rows));self.assertEqual(rows,before)
  self.assertEqual([r['record_id'] for r in result],[2,3])
  self.assertEqual(result[0]['ambient_c'],24)
 def test_audit_checks_defective_input(self):
  for cohort in DOMAINS:
   rows=dataset(cohort,99,36,True)
   self.assertEqual(pdref.audit_cleaning(rows,rows),original.audit_cleaning(rows,rows))
   self.assertEqual(pdref.audit_cleaning(rows,[])['cleaned_count'],0)
 def test_selection_empty_ties_and_boundaries(self):
  self.assertIsNone(pdref.select_model([],3,10))
  rows=[dict(name='z',validation_mae=3,latency_ms=10),dict(name='a',validation_mae=3,latency_ms=10)]
  self.assertEqual(pdref.select_model(rows,3,10),'a')
  self.assertIsNone(pdref.select_model(rows,3,9))
 def test_missing_adapter(self):
  rows=dataset('CML3111',17,36,True)
  self.assertEqual(pdref.records_from_table(pdref.pd.DataFrame(rows)),rows)
 def test_pandas_in_isolated_grader_all_cohorts(self):
  source=Path(pdref.__file__).read_text()
  for cohort in DOMAINS:
   with tempfile.TemporaryDirectory() as td:
    path=Path(td)/'99_TEST_000_DEMO-X_TEST2.ipynb'
    path.write_text(json.dumps({'cells':[dict(cell_type='code',source='STUDENT_ID="99/TEST/000/DEMO-X"\nCOHORT='+repr(cohort)+'\n'+source)]}))
    for aid in ('W06','W08','W09','W10','W11','W12','TEST1','TEST2','DA_PROJECT','ML_PROJECT'):
     result=grade_one(str(path),str(G/'specs'/f'spec_{aid}.py'),str(G/'specs/hidden'/f'spec_{aid}_hidden.py'),aid,cohort,None,15,60,None)
     self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),json.loads((ROOT/'IUEA_Teaching_Plan/assessment_banks/assessment_components.json').read_text())[aid]['deterministic_maximum'],(cohort,aid,result))

if __name__=='__main__':unittest.main()
