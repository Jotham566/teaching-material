"""Prevent terse syntax mentions from replacing the taught foundation sequence."""
import contextlib,io,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
class ExplicitFoundationsTests(unittest.TestCase):
 def order(self,week,titles):
  for d in D:
   if d['week']!=week:continue
   actual=[s['title'] for s in d['slides']]
   indexes=[actual.index(t) for t in titles]
   self.assertEqual(indexes,sorted(indexes),(d['cohort'],titles))
 def test_arithmetic_is_taught_before_combined_formula(self):
  self.order(3,['Week 3 continuation','Reading a Python expression','Addition subtraction multiplication and division','Run the four arithmetic operations','Floor division remainder and powers','Run floor division remainder and powers','Trace an expression before its output','The calculation in Python'])
 def test_decision_paths_before_functions(self):
  self.order(3,['A comparison produces a Boolean value','Comparing sizes and boundaries','Display comparison results','A condition and an if block','An if statement without else','Trace both paths through if','else gives the other path','A decision needs a colon and indentation','Trace both paths through if else','More than two branches','Tracing an if elif else chain','Trace the if elif else chain','Combining and reversing conditions','Check a permitted range','Function'])
 def test_loop_trace_before_combined_record_processing(self):
  self.order(4,['A loop repeats instructions','Read every part of a for header','Visit each item without calculating','Trace the for loop item by item','Lists loops and records in Python','A while loop checks before each repetition','A while loop with a stopping condition','Trace the while condition and update','Preventing an endless loop','continue and break change a loop’s path','Skip one item using continue','Stop at one item using break','A record and a growing list in Python'])
 def test_late_prerequisites_precede_use(self):
  self.order(5,['Read each step of a pandas chain','Calculate one total for each building'])
  self.order(6,['Testing for None and importing one tool','Cleaning decisions and charts in Python (1/2)'])
  self.order(8,['Pair two lists using zip','Inspect the pairs before measuring errors','Two error measures in Python (1/2)'])
  self.order(12,['Pass a function as the sorting key','Sorting with a tie-break rule in Python'])
 def test_tiny_examples_match_printed_answers(self):
  tested=set()
  for d in D:
   for s in d['slides']:
    if 'expected_stdout' not in s:continue
    source=s['practice_code']
    if source in tested:continue
    stream=io.StringIO()
    with contextlib.redirect_stdout(stream):exec(compile(source,s['title'],'exec'),{})
    self.assertEqual(stream.getvalue(),s['expected_stdout'],s['title']);tested.add(source)
  self.assertGreaterEqual(len(tested),15)
 def test_notes_do_not_keep_old_unrelated_explanations(self):
  for d in D:
   if d['week']<3:continue
   for s in d['slides']:
    self.assertNotIn('LECTURER DETAIL',s['notes'])
    self.assertEqual(s['notes'].count('\nNEXT\n'),1)
    if s['title']=='Reading NumPy results':self.assertNotIn('false negative',s['notes'])
if __name__=='__main__':unittest.main()
