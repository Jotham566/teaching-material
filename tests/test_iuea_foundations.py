"""Teaching-order checks for the new prerequisite sequence and unchanged contracts."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
class FoundationsTests(unittest.TestCase):
 def test_collections_before_indexing_examples(self):
  for d in D:
   if d['week']!=3:continue
   titles=[s['title'] for s in d['slides']]
   self.assertLess(titles.index('Lists dictionaries tuples and sets'),titles.index('Selecting a largest error without loops in Python'))
   self.assertLess(titles.index('A method belongs to a value'),titles.index('Find a position, then recover the original values'))
   self.assertLess(titles.index('Tracing an if elif else chain'),titles.index('Function'))
 def test_container_operations_before_records(self):
  for d in D:
   if d['week']!=4:continue
   titles=[s['title'] for s in d['slides']]
   for prerequisite in ['A dictionary is a record with named fields','Tuples and unpacking','A set remembers distinct items','Built-in summaries of a list']:
    self.assertLess(titles.index(prerequisite),titles.index('A record and a growing list in Python'))
 def test_no_live_partner_tasks(self):
  for d in D:
   if d['week']<3:continue
   for s in d['slides']:
    self.assertNotEqual(s['kind'],'activity')
    visible=' '.join(str(s.get(k,'')) for k in ['body','caption','check','title'])
    self.assertNotRegex(visible,re.compile(r'partner|swap roles|exchange your|make four cards|peer feedback',re.I))
 def test_quiz_window_and_assignment_due_date(self):
  for d in D:
   if d['week']<3:continue
   quiz=[s for s in d['slides'] if s.get('url')==d.get('quiz_url') and s.get('url')]
   for s in quiz:self.assertIn('24 hours from activation',s['body'])
   if d['cohort']=='CML3112' and d['week']==3:
    submission=next(s for s in d['slides'] if s['title']=='Engineering functions submission')
    self.assertIn('29 Sep 2026, 11:00',submission['body'])
 def test_continuation_and_complete_source(self):
  relevant=[d for d in D if d['week']>=3];self.assertEqual(len(relevant),39)
  d=next(d for d in relevant if d['cohort']=='CML3112' and d['week']==3)
  self.assertEqual(d['slides'][11]['title'],'Names, conversion and comments')
  self.assertEqual(d['slides'][12]['title'],'Week 3 continuation')
  for d in relevant:
   for i,s in enumerate(d['slides'],1):
    self.assertEqual(s['sequence_number'],i)
    self.assertIn('Explanation to give',s['notes'])
if __name__=='__main__':unittest.main()
