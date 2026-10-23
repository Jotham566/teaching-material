"""Regression checks for partial credit, boundary values and authentic plots."""
import ast,inspect,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];G=ROOT/'IUEA_Teaching_Plan/grader';sys.path.insert(0,str(G))
import test1_coding_contracts as contract
import test1_coding_reference as reference
from isolated_grading import decode
from batch_grade import grade_one
class NS:
 def __init__(self, **overrides):self.overrides=overrides
 def get(self,name,default=None):return self.overrides.get(name,'CML3112' if name=='COHORT' else getattr(reference,name,default))
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
 def test_cleaning_failure_does_not_zero_other_tasks(self):
  folder=G.parent/'assessment_banks/TEST1/CML3111/A'
  nb=json.loads((folder/'TEST1_student.ipynb').read_text())
  source=(G/'test1_coding_reference.py').read_text()
  for c in nb['cells']:
   text=''.join(c['source'])
   if c['cell_type']=='code' and text.startswith('def '):
    c['source']=source+'\ndef clean_observations(input_records):\n    raise ValueError("unfinished")\n'
  with tempfile.TemporaryDirectory() as temp:
   p=Path(temp)/'partial.ipynb';p.write_text(json.dumps(nb))
   result=grade_one(str(p),str(G/'specs/spec_TEST1.py'),str(G/'specs/hidden/spec_TEST1_hidden.py'),'TEST1','CML3111',str(folder),20,180,None)
  self.assertEqual(sum(q['awarded'] for q in result['questions'].values()),80,result)
if __name__=='__main__':unittest.main()
