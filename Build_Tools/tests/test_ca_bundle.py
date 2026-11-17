import io,json,zipfile
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from ca_bundle import verify_bundle
from tests import test_ca_refresh as fixtures
from tests.test_ca_refresh import receipt,manifest,sha,dump
import refresh_ca as runner

class BundleTests(unittest.TestCase):
    setUp=fixtures.RefreshTests.setUp
    fake_grade=fixtures.RefreshTests.fake_grade
    fake_render=fixtures.RefreshTests.fake_render
    def bundle(self):
        members={};old=receipt();old['timing_status']='ON_TIME';new=receipt('two','file2');new.update(submitted_at='2026-10-02T09:00:00Z',timing_status='ON_TIME')
        for c in runner.COHORTS:
            for i in range(1,6):
                m=manifest([]);m.update(key=f'{c}|W{i:02}',files=[])
                if c=='CML3111' and i==3:
                    m=manifest([old,new]);m['files'].append(dict(id='file2',sha256=sha(b'second'),export_name='file2.bin'))
                    buf=io.BytesIO()
                    with zipfile.ZipFile(buf,'w') as z:z.writestr('file1.bin',b'first');z.writestr('file2.bin',b'second')
                    members['CML3111_W03_files_1.zip']=buf.getvalue()
                members[f'{c}_W{i:02}_manifest.json']=json.dumps(m).encode()
                members[f'{c}_Q{i}_quiz.json']=json.dumps(dict(exported_at='2026-10-20T00:00:00Z',source_kind='recorded_sheet_scores_with_form_receipts',quizzes=[dict(key=f'{c}|{i}',items=[dict(id='recorded-total',points=5)],records=[])])).encode()
        members['quiz_deadlines.json']=json.dumps({f'{c}|{i}':{'closeAt':1793404800000} for c in runner.COHORTS for i in range(1,6)}).encode()
        meta=dict(format='IUEA_CA_BUNDLE',version=1,complete=True,cutoff='2026-10-20T00:00:00Z',files=[dict(name=n,sha256=sha(b),bytes=len(b)) for n,b in members.items()])
        members['ca_bundle.json']=json.dumps(meta).encode()
        path=self.root/'IUEA_CA.zip'
        with zipfile.ZipFile(path,'w') as z:
            for n,b in members.items():z.writestr(n,b)
        return path,members

    def test_one_zip_without_excel_files(self):
        path,_=self.bundle();verify_bundle(path)
        runner.refresh(path,self.private,grader=self.fake_grade,renderer=self.fake_render)
        self.assertEqual(len(runner.read(self.private/'ledger.json')['attempts']),2)
        runner.refresh(path,self.private,grader=lambda *x:self.fail('Duplicate grade'),renderer=self.fake_render)

    def test_corrupt_and_missing_member_rejected(self):
        path,members=self.bundle()
        members['quiz_deadlines.json']=b'{}'
        with zipfile.ZipFile(path,'w') as z:
            for n,b in members.items():z.writestr(n,b)
        with self.assertRaisesRegex(ValueError,'checksum'):verify_bundle(path)
        del members['quiz_deadlines.json']
        with zipfile.ZipFile(path,'w') as z:
            for n,b in members.items():z.writestr(n,b)
        with self.assertRaisesRegex(ValueError,'inventory'):verify_bundle(path)

    def test_duplicate_member_rejected(self):
        import warnings
        path,_=self.bundle()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(path,'a') as z:z.writestr('quiz_deadlines.json',b'{}')
        with self.assertRaisesRegex(ValueError,'duplicate'):verify_bundle(path)

if __name__=='__main__':unittest.main()
