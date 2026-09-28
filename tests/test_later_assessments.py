import json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader'
sys.path.insert(0,str(G))
from batch_grade import grade_one
from engineering_contracts import TASKS,check,DOMAINS
import engineering_reference as ref
class LaterAssessmentTests(unittest.TestCase):
 def test_component_totals(self):
  config=json.loads((ROOT/'IUEA_Teaching_Plan/assessment_banks/assessment_components.json').read_text())
  for aid,cfg in config.items():
   original=json.loads((G/'rubrics'/f'{aid}.json').read_text());hybrid=json.loads((G/'rubrics/hybrid'/f'{aid}.json').read_text())
   for c in original['criteria']:
    numerical=sum(x['marks'] for x in cfg['criterion_allocation'] if x['criterion']==c['id'])
    reasoning=sum(x['maximum'] for x in hybrid['criteria'] if x.get('parent_criterion',x['id'])==c['id'])
    self.assertEqual(numerical+reasoning,c['maximum'])
   self.assertEqual(cfg['deterministic_maximum']+cfg['reasoning_maximum'],cfg['maximum'])
 def test_unseen_inputs_reject_constants(self):
  class NS:
   def get(self,name,default=None):return 'CML3111' if name=='COHORT' else lambda *args:{}
  for task in TASKS:self.assertFalse(check(NS(),task)[0],task)
 def test_reference_contracts_in_docker_all_cohorts(self):
  source=Path(ref.__file__).read_text()
  for cohort in DOMAINS:
   with tempfile.TemporaryDirectory() as d:
    path=Path(d)/'99_TEST_000_DEMO-X_TEST2.ipynb'
    path.write_text(json.dumps({'cells':[dict(cell_type='code',source='STUDENT_ID="99/TEST/000/DEMO-X"\nCOHORT='+repr(cohort)+'\n'+source)]}))
    for aid in ('W06','W08','W09','W10','W11','W12','TEST1','TEST2','DA_PROJECT','ML_PROJECT'):
     r=grade_one(str(path),str(G/'specs'/f'spec_{aid}.py'),str(G/'specs/hidden'/f'spec_{aid}_hidden.py'),aid,cohort,None,15,60,None)
     self.assertEqual(sum(x['awarded'] for x in r['questions'].values()),json.loads((ROOT/'IUEA_Teaching_Plan/assessment_banks/assessment_components.json').read_text())[aid]['deterministic_maximum'],(cohort,aid,r))
if __name__=='__main__':unittest.main()

class PlotEvidenceTests(unittest.TestCase):
 def test_submitted_metadata_is_not_a_rendered_figure(self):
  from isolated_grading import decode,PlotEvidence
  forged=decode({'type':'mapping','items':[['plot_axes',[]]]})
  real=decode({'type':'figure','axes':[]})
  self.assertNotIsInstance(forged,PlotEvidence)
  self.assertIsInstance(real,PlotEvidence)
