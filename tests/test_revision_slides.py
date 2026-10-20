"""Execute advance-revision examples and check six deck briefings."""
import json,os,tempfile,unittest,shutil
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
ROOT=Path(__file__).resolve().parents[1]
class RevisionSlides(unittest.TestCase):
 def test_all_revision_examples(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  selected=[d for d in decks if d['week'] in (7,14)]
  self.assertEqual(len(selected),6)
  original=Path.cwd()
  for d in selected:
   with tempfile.TemporaryDirectory() as tmp:
    os.chdir(tmp)
    try:
     exam=1 if d['week']==7 else 2
     filename=f"{d['cohort']}_Test{exam}_practice.csv"
     shutil.copy(ROOT/'IUEA_Teaching_Plan/test_revision'/d['cohort']/f'Test{exam}'/filename,tmp)
     ns={}
     for s in d['slides']:
      if s.get('revision_example'):
       exec(s.get('practice_code',s['code']),ns);exec(s.get('revision_check',''),ns)
     self.assertTrue(Path(filename).exists())
     if exam==1:
      small=ns['revision_clean'](ns['original_records'][:2])
      summary=ns['revision_summary'](small)
      self.assertEqual(summary['count'],2)
      self.assertEqual(summary['mean'],15)
      self.assertEqual(ns['revision_findings'](small)['group_gap']['value'],0)
      self.assertEqual(small[1]['ambient'],20)
      self.assertIsNone(ns['original_records'][1]['ambient'])
     import matplotlib.pyplot as plt
     plt.close('all')
    finally:os.chdir(original)
   visible='\n'.join(str(s.get(k,'')) for s in d['slides'] for k in ('title','body','code','caption'))
   full=json.dumps(d)
   for stale in ['A, B or C answers','My written evidence','code execution prohibited','Part B is typed']:
    self.assertNotIn(stale,full)
   self.assertIn('Downloads unlock at the scheduled start time',visible)
   self.assertIn(filename,visible)
   self.assertTrue(all(s.get('notes') for s in d['slides']))
   links=[s for s in d['slides'] if s.get('kind')=='test_entry']
   self.assertEqual(len(links),1)
   self.assertIn(d['cohort']+'%7CTEST'+('1' if d['week']==7 else '2'),links[0]['url'])
if __name__=='__main__':unittest.main()
