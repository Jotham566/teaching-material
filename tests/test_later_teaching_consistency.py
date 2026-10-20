"""Guard the beginner sequence and the slide/notebook/package agreement."""
import ast,json,sys,unittest,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from descriptive_teaching_names import operations
class LaterTeaching(unittest.TestCase):
 def test_later_decks_and_notebooks(self):
  decks=[d for d in json.loads((ROOT/'data/iuea_deck_content.json').read_text()) if d['week']>=8]
  self.assertEqual(len(decks),24)
  for d in decks:
   with self.subTest(cohort=d['cohort'],week=d['week']):
    seen=set();expected=[];past_assignment=False
    for index,s in enumerate(d['slides'],1):
     self.assertEqual(s['sequence_number'],index)
     seen.update(s.get('introduced_operations',[]))
     if s['title'] in ('Your issued assignment','Your issued task','Ungraded cleaning practice'):past_assignment=True
     program=s.get('practice_code','')
     if program:
      self.assertTrue(set(operations(program)).issubset(seen),set(operations(program))-seen)
      ast.parse(program)
      self.assertIn('Verified result with the supplied CSV',s['notes'])
      if not past_assignment:expected.append(program.strip())
     if s.get('code'):
      self.assertLessEqual(len(s['code'].splitlines()),8)
    if d['week']<=14:
     nbpath=ROOT/'IUEA_Teaching_Plan/guided_practice'/d['cohort']/f"W{d['week']:02}"/'guided_practice.ipynb'
     nb=json.loads(nbpath.read_text())
     actual=[''.join(c['source']).strip() for c in nb['cells'] if c['cell_type']=='code']
     self.assertEqual(actual,expected)
     if d['week']<=12:
      with zipfile.ZipFile(ROOT/'IUEA_Teaching_Plan/student_packages'/f"{d['cohort']}_W{d['week']:02}_student.zip") as z:
       self.assertEqual(z.read('guided_practice.ipynb'),nbpath.read_bytes())
       self.assertFalse(any('grader' in n.lower() for n in z.namelist()))
if __name__=='__main__':unittest.main()
