"""Keep lesson data sources and the distributed notebooks in sync."""
import ast,json,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CsvLessonTests(unittest.TestCase):
 def test_file_sources_and_no_invented_observation_tables(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  for d in decks:
   if not d.get('csv_examples_revision'):continue
   w=d['week'];cohort=d['cohort'];source={7:6,14:12}.get(w,w)
   folder=ROOT/'IUEA_Teaching_Plan'/('practicals' if w<=5 else 'assessment_banks')/f'W{source:02}'/cohort
   if w>5:folder=folder/'A'
   programs=[s['practice_code'] for s in d['slides'] if s['kind']=='code' and s.get('practice_code')]
   loads=[]
   for program in programs:
    for node in ast.walk(ast.parse(program)):
     if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='read_csv':
      path=ast.literal_eval(node.args[0]);self.assertTrue((folder/path).is_file(),(cohort,w,path));loads.append(path)
     if w>=5 and isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='DataFrame' and node.args and isinstance(node.args[0],ast.Dict):
      # A candidate table may hold a name, but numeric evidence must be computed.
      for value in node.args[0].values:
       if isinstance(value,ast.List):self.assertFalse(any(isinstance(x,ast.Constant) and isinstance(x.value,(int,float)) for x in value.elts),(cohort,w,program))
   if w>=5:self.assertTrue(loads,(cohort,w))
 def test_student_zip_matches_current_practice(self):
  base=ROOT/'IUEA_Teaching_Plan'
  for cohort in ('CML3111','CML3112','CML3113'):
   for week in (4,5,6,8,9,10,11,12):
    with zipfile.ZipFile(base/f'student_packages/{cohort}_W{week:02}_student.zip') as z:
     self.assertEqual(z.read('guided_practice.ipynb'),(base/f'guided_practice/{cohort}/W{week:02}/guided_practice.ipynb').read_bytes())
     self.assertFalse(any('grader' in n.lower() or n.endswith('.py') for n in z.namelist()))
if __name__=='__main__':unittest.main()
