import hashlib,json,re,sys,unittest,zipfile,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from slide_note_explanations import explanation
from reviewed_notes_overlay import apply_slide_specific_notes
A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
class SpecificNotes(unittest.TestCase):
 def test_similar_words_do_not_select_unrelated_explanations(self):
  self.assertIn('ablation',explanation('Feature comparisons in Python')[0])
  self.assertIn('mask',explanation('A comparison creates a Boolean mask')[0].lower())
  self.assertIn('ranking',explanation('Sorting with a tie-break rule')[0])
  self.assertIn('model object',explanation('Regression models and errors in Python continued')[0])
  self.assertIn('ZIP',explanation('The files in your ZIP')[0])
 def test_current_decks_match_manifest_and_have_specific_notes(self):
  rows=json.loads((ROOT/'data/iuea_lecturer_notes_manifest.json').read_text())
  self.assertEqual(len(rows),45)
  for row in rows:
   p=ROOT/'IUEA_Teaching_Plan/decks'/row['filename'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),row['sha256'])
   with zipfile.ZipFile(p) as z:
    notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+.xml',n)]
    self.assertEqual(len(notes),row['slides'])
    for n in notes:
     text='\n'.join(t.text or '' for t in E.fromstring(z.read(n)).iter(A+'t'))
     self.assertIn('Explanation to give',text)
     self.assertIn('Worked illustration / lecturer answer',text)
     self.assertNotIn('Teach one example, pause for every learner to predict',text)
     self.assertNotIn('Move on after a learner can explain the current example',text)
 def test_source_overlay_rejects_stale_slide_notes(self):
  decks=json.loads((ROOT/'data/iuea_deck_content.json').read_text())
  apply_slide_specific_notes(decks)
  decks[0]['slides'][0]['title']='Changed lesson'
  with self.assertRaises(ValueError):apply_slide_specific_notes(decks)
if __name__=='__main__':unittest.main()
