"""Protect the student-facing instruction contract without changing the grader."""
import json,re,sys,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from assessment_registry import records
from concise_iuea_assignments import WRITTEN,COMPONENTS,TASKS
B=ROOT/'IUEA_Teaching_Plan'
class ClearAssignments(unittest.TestCase):
 def test_all_iuea_forms_have_short_exact_upload_lists(self):
  data=json.loads((ROOT/'data/iuea_assignment_form_briefs.json').read_text())
  self.assertEqual(set(data),{r['key'] for r in records() if r['cohort']!='DA'})
  for key,row in data.items():
   self.assertLessEqual(len(row['brief'].split()),200,key)
   self.assertIn('WHAT TO UPLOAD',row['brief'])
   self.assertNotIn('Award ',row['brief'])
   if key.endswith(('W03','W04','W05')):self.assertIn('No separate report',row['brief'])
 def test_every_written_mark_has_a_student_prompt(self):
  for aid,items in WRITTEN.items():
   rubric=json.loads((B/'grader/rubrics/hybrid'/f'{aid}.json').read_text())
   self.assertEqual({k for k,_ in items},{c['id'] for c in rubric['criteria']},aid)
   for cohort in ['CML3111','CML3112','CML3113']:
    nb=json.loads((B/'assessment_banks'/aid/cohort/'A'/f'{aid}_student.ipynb').read_text())
    text='\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='markdown')
    self.assertEqual(text.count('<!-- assignment-workflow -->'),1)
    for _,prompt in items:self.assertIn(prompt,text)
    self.assertNotIn('Award ',text)
    for part in COMPONENTS[aid]['criterion_allocation']:self.assertIn(TASKS[part['task']][0],text)
 def test_packages_have_the_same_current_instructions(self):
  for cohort in ['CML3111','CML3112','CML3113']:
   for week in [2,3,4,5,6,8,9,10,11,12]:
    with zipfile.ZipFile(B/'student_packages'/f'{cohort}_W{week:02}_student.zip') as z:
     guide=(B/'student_guides'/cohort/f'W{week:02}.md').read_text()
     self.assertEqual(z.read('ASSIGNMENT_INSTRUCTIONS.txt').decode(),guide)
     self.assertNotIn('READ_INSTRUCTIONS_FIRST.txt',z.namelist())
     self.assertFalse(any('/hidden/' in n or '_hidden.py' in n or 'solution' in n.lower() for n in z.namelist()))
     allowed_scripts={'hello_engineering.py'} if week==2 else set()
     self.assertEqual({n for n in z.namelist() if n.endswith('.py')},allowed_scripts)
     if week in (3,5):
      self.assertIn('No grading scripts are needed.',guide)
     name='proof_of_life.ipynb' if week==2 else f'W{week:02}_student.ipynb'
     nb=json.loads(z.read(name))
     self.assertNotRegex('\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code'),r'iuea_grader|spec_W\d+|g\.check\(')
     self.assertIn(guide,''.join(nb['cells'][1]['source']))
     for c in nb['cells']:
      if c['cell_type']=='code':self.assertFalse(c['outputs'])
 def test_progress_and_existing_a3_reopening(self):
  p=(B/'Teaching_Progress.md').read_text()
  self.assertIn('All Week 3 content completed',p)
  self.assertEqual(p.count('Week 3 not yet taught'),2)
  for code in ['CML3111','CML3112','CML3113']:
   nb=json.loads((B/'practicals/W03'/code/'W03_student.ipynb').read_text())
   prompts=[''.join(c['source']) for c in nb['cells'] if c['cell_type']=='markdown']
   self.assertEqual(sum(bool(re.match(r'## q[1-5]:',s)) for s in prompts),5)
   self.assertIn('A loop is not required.','\n'.join(prompts))
  self.assertIn('30 September 2026, 11:27',(B/'student_guides/CML3112/W03.md').read_text())
if __name__=='__main__':unittest.main()
