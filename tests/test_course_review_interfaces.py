"""Assessment output labels must remain compatible with the published grader."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class AssessmentSlideInterfaces(unittest.TestCase):
 def test_required_labels(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  expected={'predict_regression':('baseline','linear','tree'),'classification_metrics':('tp','tn','fp','fn','precision','recall','cost'),'ablation_metrics':('base_mae','extended_mae','improvement'),'select_model':('name','validation_mae','latency_ms')}
  found={key:0 for key in expected}
  for d in decks:
   for s in d['slides']:
    if s['kind']!='contract':continue
    key=s['title'].split('(')[0]
    if key in expected:
     found[key]+=1
     with self.subTest(cohort=d['cohort'],week=d['week'],function=key):
      for token in expected[key]:self.assertRegex(s['body'],r'\b'+token+r'\b')
      for renamed in ('tree_model','base_absolute_error','prediction_time_ms','true_positive_count'):
       self.assertNotIn(renamed,s['body'])
  self.assertTrue(all(found.values()))
 def test_no_legacy_offline_tests(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  for d in decks:
   visible='\n'.join(s.get('body','') for s in d['slides'])
   self.assertNotIn('Rehearse offline TEST2',visible)
   self.assertNotIn('Return three prediction lists under baseline, linear and tree_model',visible)
if __name__=='__main__':unittest.main()
