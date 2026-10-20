import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from pandas_explanations import operations
class PrerequisiteTests(unittest.TestCase):
 def test_new_operation_cannot_silently_skip_explanation(self):
  with self.assertRaisesRegex(ValueError, 'prerequisite explanation'):
   operations('selected = raw.query("load_pct > 20")')
 def test_operations_precede_code_and_notes_explain_results(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text());count=0
  for d in decks:
   if not d.get('pandas_explanations_revision'):continue
   # Exam revision decks have a separate executable-example regression test.
   if d['week'] in (6,7,14):continue
   count+=1;introduced=set();program=''
   for i,s in enumerate(d['slides'],1):
    introduced.update(s.get('introduced_operations',[]))
    self.assertEqual(s['sequence_number'],i)
    if s['kind']!='code':continue
    program=s.get('practice_code') or program
    self.assertFalse(set(operations(program))-introduced,(d['cohort'],d['week'],i))
    if d.get('common_ml_names'):
     self.assertIn('Step-by-step explanation',s['notes'])
     self.assertIn('Verified result with the supplied CSV',s['notes'])
    elif d.get('full_course_review_revision'):
     self.assertIn('Result from the supplied example',s['notes'])
     self.assertTrue(s.get('expected_output'))
    else:
     self.assertTrue('Code walkthrough\n' in s['notes'] or 'Line 1:' in s['notes'])
     if 'Code walkthrough\n' in s['notes']:
      self.assertIn('Output from the supplied CSV',s['notes'])
     else:
      self.assertGreater(len(s['notes']),100)
    self.assertNotIn('Run the example to display the current result.',s['notes'])
  self.assertEqual(count,18)  # CML3113 W6 has its own executable beginner-workflow test.
if __name__=='__main__':unittest.main()
