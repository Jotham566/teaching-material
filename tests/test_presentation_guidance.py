"""Prevent conflicting student-facing submission and quiz instructions returning."""
import unittest,zipfile,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DECKS=ROOT/'IUEA_Teaching_Plan/decks';A='{http://schemas.openxmlformats.org/drawingml/2006/main}'
def slide(path,number):
 with zipfile.ZipFile(path) as z:
  root=E.fromstring(z.read(f'ppt/slides/slide{number}.xml'))
 return '\n'.join(''.join(t.text or '' for t in p.iter(A+'t')) for p in root.iter(A+'p'))
class GuidanceTests(unittest.TestCase):
 def test_historical_quiz_window_is_unconditional(self):
  for p in DECKS.glob('*Week01*.pptx'):
   text=slide(p,56);self.assertIn('24 hours from lecturer activation',text);self.assertNotIn('if the network fails',text)
  text=slide(DECKS/'CML3112_Week02_Design_Infrastructure.pptx',43)
  self.assertIn('24 hours from lecturer activation',text)
 def test_week2_browser_route_does_not_require_local_git(self):
  text=slide(DECKS/'CML3112_Week02_Design_Infrastructure.pptx',30)
  self.assertIn('Add file -> Upload files: notebook and CSV',text)
  self.assertIn('not Python cells',text)
  self.assertNotIn('name it exactly as given on the next slide',text)
 def test_week2_readme_and_upload_set_are_current(self):
  p=DECKS/'CML3112_Week02_Design_Infrastructure.pptx'
  self.assertIn('Upload only your notebook and README.md',slide(p,31))
  self.assertIn('How to open the notebook, upload the CSV and run cells from the top',slide(p,32))
  self.assertNotIn('By Week 13',slide(p,32))
 def test_project_report_is_not_confused_with_test_notebook(self):
  for p in DECKS.glob('*Week08*.pptx'):
   with zipfile.ZipFile(p) as z:
    text=' '.join(t.text or '' for name in z.namelist() if name.startswith('ppt/slides/slide') and name.endswith('.xml') for t in E.fromstring(z.read(name)).iter(A+'t'))
   self.assertIn('separate readable DOCX/PDF report',text)
if __name__=='__main__':unittest.main()
