"""Equivalent unit spellings must pass; wrong dimensions and plots must fail."""
import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
from engineering_contracts import unit_matches,measurement_same
from colab_exam_contracts import decision_keys
from batch_grade import grade_one
import engineering_pandas_reference as ref
class UnitTests(unittest.TestCase):
 def test_unit_spelling_and_boundaries(self):
  for u in ['deg C','degrees C','degree Celsius','°C','℃','celsius']:
   self.assertTrue(unit_matches(u,'deg C'),u)
   self.assertTrue(unit_matches('Temperature ('+u+')','deg C',label=True),u)
   self.assertTrue(measurement_same({'value':25,'unit':u},{'value':25.,'unit':'deg C'}))
  for bad in ['°F','K','kW','25 deg C','notdeg C']:
   self.assertFalse(unit_matches(bad,'deg C'),bad)
  for label in ['Target (kWh/t)','Target (MW)','Target (kW/h)']:
   self.assertFalse(unit_matches(label,'kW',label=True),label)
  self.assertFalse(measurement_same({'value':30,'unit':'°C'},{'value':25,'unit':'deg C'}))
 def test_real_figures_and_findings_in_docker(self):
  source=Path(ref.__file__).read_text()
  cases=[('CML3111',u,100) for u in ['°C','degrees C','degree Celsius']]
  cases += [('CML3111','°F',69),('CML3112','kWh/t',69),('CML3113','kW',69)]
  for cohort,unit,expected in cases:
   original={'CML3111':'deg C','CML3112':'kW','CML3113':'kWh/t'}[cohort]
   solution=source.replace(repr(cohort)+':'+repr(original),repr(cohort)+':'+repr(unit))
   nb={'cells':[{'cell_type':'code','source':'STUDENT_ID="DEMO-UNIT-CHECK"\nCOHORT='+repr(cohort)+'\n'+solution+'\nDECISIONS='+repr(decision_keys()['TEST1'])}]}
   with tempfile.TemporaryDirectory() as tmp:
    p=Path(tmp)/'DEMO-UNIT-CHECK_TEST1.ipynb';p.write_text(json.dumps(nb))
    r=grade_one(str(p),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1',cohort,None,20,120,None)
    self.assertEqual(sum(q['awarded'] for q in r['questions'].values()),expected,(cohort,unit,r))
if __name__=='__main__':unittest.main()
