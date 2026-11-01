import sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import evidence_extract as e
import continuous_assessment as ca


class EvidenceExtract(unittest.TestCase):
    def test_utf16_readme_and_zip_saved_as_bin(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);md=d/'a.md'
            md.write_bytes(('Restart the runtime and run all cells from the top, then save.').encode('utf-16'))
            self.assertIn('Restart the runtime',e.extract(md,'W02'))
            z=d/'x.bin'
            with zipfile.ZipFile(z,'w') as f:
                f.writestr('r/README.md','Run all cells from the top after restart to get the right answer.')
                f.writestr('../evil.md','Escaped member that must never be read by the extractor at all.')
            text=e.extract(z,'W02')
            self.assertIn('README.md',text);self.assertNotIn('evil',text)

    def test_lecturer_test_rows_are_recognised(self):
        t=lambda **k:ca.is_lecturer_test(dict(student_id='24/1/BSCE-S',email='a@b.c',full_name='A B',**k))
        self.assertTrue(t(submitted_student_id='TEST005'))
        self.assertTrue(ca.is_lecturer_test(dict(student_id='X',email='WirmbeeSubs@gmail.com',full_name='')))
        self.assertTrue(ca.is_lecturer_test(dict(student_id='X',email='a@b.c',full_name='Martin Wambi')))
        self.assertFalse(t(submitted_student_id='24/1/BSCE-S'))


if __name__=='__main__':unittest.main()
