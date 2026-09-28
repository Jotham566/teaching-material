"""Prerequisite and delivery regressions for the published teaching sequence."""
import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'review/2026-09-15/ppt-revision/deck-content.json').read_text())
class SequenceTests(unittest.TestCase):
 def test_foundations_precede_practice(self):
  checks={2:[('Give a value a name','Worked example')],3:[('Start with numbers and values','Names, conversion and comments'),('Condition','A decision needs a colon and indentation'),('Function','Positional and named inputs'),('Selecting a largest error without loops','Reading a short list')],4:[('List and index','A list stores items in order'),('Dictionary','A dictionary gives each value a key'),('with and import','Open a real CSV and inspect its first row')],5:[('Mask and filter','Keep rows where the comparison is true')],8:[('Rows and arrays before model code','Rows, columns and named options'),('A model object keeps learned information','Worked example')],9:[('State the cost rule before calculating','Worked example')],10:[('Cross-validation','Each fold takes a turn at validation')],11:[('Read the physical example across programmes','An interaction uses two known inputs')],12:[('A tuple supplies an ordered ranking key','Sorting with a tie-break rule in Python')],13:[('Read the path example','Worked example')]}
  for d in D:
   titles=[s['title'] for s in d['slides']]
   for before,after in checks.get(d['week'],[]):
    with self.subTest(cohort=d['cohort'],week=d['week'],before=before):
     a=next(i for i,t in enumerate(titles) if t==before or t.startswith(before+' ('))
     b=next(i for i,t in enumerate(titles) if t==after or t.startswith(after+' ('))
     self.assertLess(a,b)
 def test_practice_code_matches_slide_order_exactly(self):
  for d in D:
   if d['week'] not in (3,4,5,6,8,9,10,11,12):continue
   slide_code=[s['practice_code'].strip() for s in d['slides'] if s.get('practice_code')]
   p=ROOT/'IUEA_Teaching_Plan/guided_practice'/d['cohort']/f"W{d['week']:02}"/'guided_practice.ipynb'
   nb=json.loads(p.read_text());notebook_code=[''.join(c['source']).strip() for c in nb['cells'] if c['cell_type']=='code']
   self.assertEqual(slide_code,notebook_code,(d['cohort'],d['week']))
 def test_week2_catchup_links_and_deadlines(self):
  links=json.loads((ROOT/'data/submission_links.json').read_text());quizzes=json.loads((ROOT/'data/quiz_links.json').read_text())
  for d in D:
   if d['week']!=2:continue
   urls=[s.get('url') for s in d['slides']]
   for key in ('W01','W02'):self.assertIn(links[d['cohort']+'|'+key]['url'],urls)
   for key in ('1','2'):self.assertIn(quizzes[d['cohort']+'|'+key],urls)
   self.assertEqual(links[d['cohort']+'|W01']['closeAt'],links[d['cohort']+'|W02']['closeAt'])
   self.assertIn('24 hours',next(s['body'] for s in d['slides'] if s['title']=='Week 1 Quiz 1 catch-up'))
 def test_every_original_slide_accounted_for(self):
  audit=json.loads((ROOT/'review/2026-09-16/sequential/sequence-audit.json').read_text())
  self.assertEqual(len(audit),41)
  self.assertEqual(sum(r['reviewed_original_slides'] for r in audit),1544)
  self.assertEqual(sum(r['final_slides'] for r in audit),sum(len(d['slides']) for d in D))
if __name__=='__main__':unittest.main()
