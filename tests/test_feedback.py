import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from export_feedback import page
class FeedbackTests(unittest.TestCase):
 def test_unresolved_is_not_zero_and_html_is_escaped(self):
  content=page('<script>x</script>',dict(status='EXCEPTION',score=None,maximum=20),dict(id='W02-test',title='Test',criteria=[]))
  self.assertIn('not a zero',content);self.assertNotIn('<script>',content);self.assertIn('&lt;script&gt;',content)
 def test_gate_is_visible_in_final_criterion_marks(self):
  rubric=dict(id='TEST2-test',criteria=[dict(id='a',parent_criterion='c2',title='Leakage',maximum=10)])
  result=dict(status='AUTO_SCORED',score=20,maximum=100,evaluations=[dict(criteria=[dict(id='a',awarded=10,feedback='Text supplied')]) for _ in range(2)],execution_gate_adjustments=[dict(parent_criterion='c2',reason='Split failed')])
  content=page('S10001',result,rubric);self.assertIn('0 / 10',content);self.assertIn('Split failed',content)
if __name__=='__main__':unittest.main()
