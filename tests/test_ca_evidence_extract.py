import sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import evidence_extract as e
import attachment_expand as ax
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


class Expand(unittest.TestCase):
    def test_zip_members_skip_unsafe_and_junk(self):
        with tempfile.TemporaryDirectory() as d:
            d=Path(d);z=d/'s.zip'
            with zipfile.ZipFile(z,'w') as f:
                f.writestr('proj/S1_W03.ipynb','{"cells":[]}');f.writestr('../evil.ipynb','{}')
                f.writestr('__MACOSX/._a.ipynb','x');f.writestr('.ipynb_checkpoints/a-checkpoint.ipynb','{}');f.writestr('data.csv','a')
            names=[m['original_name'] for m in ax.zip_members(z,d/'c')]
            self.assertEqual(names,['S1_W03.ipynb'])

    def test_github_links_found_in_html(self):
        with tempfile.TemporaryDirectory() as d:
            h=Path(d)/'l.html';h.write_text('<a href="https://github.com/stud/week3-work/tree/main/nb">repo</a> https://github.com/features/x')
            self.assertEqual(ax.github_links(h),[('stud','week3-work','main/nb')])

class Condense(unittest.TestCase):
    def test_long_report_fits_and_is_marked(self):
        text='\n'.join(f'Line {i} '+'word '*30 for i in range(600))
        out=e.condense(text)
        self.assertLessEqual(len(out),12000)
        self.assertIn(e.CONDENSED,out)
        self.assertTrue(out.startswith('Line 0 '))
        self.assertEqual(e.condense('short'),'short')

    def test_overlong_notebook_is_condensed_not_rejected(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            nb=Path(d)/'a.ipynb'
            nb.write_text(json.dumps({'cells':[{'cell_type':'markdown','source':['# Part %d\n'%i,'text '*60]} for i in range(400)]}))
            out=e.extract(nb,'W01')
            self.assertIn(e.CONDENSED,out)

    def test_files_share_combined_budget(self):
        import prepare_ca_written as p
        with tempfile.TemporaryDirectory() as d:
            files=[]
            for i in range(2):
                f=Path(d)/f'{i}.md';f.write_text('\n'.join('row %d '%j+'x'*50 for j in range(300)))
                files.append(dict(path=str(f),text_sha256=''))
            p.share(dict(files=files))
            self.assertLess(sum(len(Path(f['path']).read_text()) for f in files),12000)


if __name__=='__main__':unittest.main()
