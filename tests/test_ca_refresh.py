"""Synthetic refresh tests: no student data, model inference or Docker needed."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import refresh_ca as runner
import continuous_assessment as ca


def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,v): runner.write(p,v)
def receipt(rid='one',fid='file1'):
    return dict(response_id=rid,assessment_key='CML3111|W03',email='synthetic@example.test',submitted_at='2026-10-01T09:00:00Z',fields={'Student Registration Number':'SYNTHETIC-ONLY'},file_ids=[fid])
def manifest(rows,content=b'first',fid='file1'):
    return dict(key='CML3111|W03',exported_at='2026-10-20T00:00:00Z',window={'open':'2026-09-01T00:00:00Z','close':'2026-10-30T00:00:00Z'},records=rows,files=[dict(id=fid,sha256=sha(content),export_name=fid+'.bin')],errors=[])

def xlsx(path,sheets):
    # Minimal synthetic XLSX fixture; date cells use Excel's built-in date style.
    from xml.sax.saxutils import escape
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1,len(sheets)+1))+'</Types>')
        z.writestr('xl/workbook.xml','<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'+''.join(f'<sheet name="{escape(name)}" sheetId="{i}" r:id="rId{i}"/>' for i,name in enumerate(sheets,1))+'</sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1,len(sheets)+1))+'<Relationship Id="styles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')
        z.writestr('xl/styles.xml','<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="1"><font/></fonts><fills count="1"><fill><patternFill/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="2"><xf numFmtId="0"/><xf numFmtId="14"/></cellXfs></styleSheet>')
        for i,rows in enumerate(sheets.values(),1):
            body=''
            for rn,row in enumerate(rows,1):
                body+=f'<row r="{rn}">'
                for cn,value in enumerate(row):
                    address=f'{chr(65+cn)}{rn}'
                    if isinstance(value,tuple):body+=f'<c r="{address}" s="1"><v>{value[0]}</v></c>'
                    elif isinstance(value,(int,float)):body+=f'<c r="{address}"><v>{value}</v></c>'
                    else:body+=f'<c r="{address}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'
                body+='</row>'
            z.writestr(f'xl/worksheets/sheet{i}.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'+body+'</sheetData></worksheet>')

class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.private=self.root/'private';self.private.mkdir()
        self.source=self.private/'reconciled';(self.source/'files').mkdir(parents=True)
        self.data=b'first';(self.source/'files/file1.bin').write_bytes(self.data)
        dump(self.source/'CML3111_W03_manifest.json',manifest([receipt()]))
        dump(self.source/'timing.json',{})
        self.old_grade=dict(cohort='CML3111',assessment='W03',student_id='SYNTHETIC-ONLY',response_id='one',score=17,status='GRADED',source_hashes={'file1':sha(self.data)})
        dump(self.private/'written_queue/combined_results.json',[self.old_grade])
        ledger=ca.build(self.source,self.private/'written_queue/combined_results.json')
        dump(self.private/'ledger.json',ledger);(self.private/runner.BOOK).write_bytes(b'original workbook')

    def test_preserve_complete_and_regrade_changed_bytes(self):
        raw=ca.build(self.source,resolve_identities=False)
        kept,todo=runner.select_work(self.source,raw,[self.old_grade]);self.assertEqual(len(kept),1);self.assertFalse(todo)
        meta=runner.read(self.source/'CML3111_W03_manifest.json');meta['files'][0]['sha256']=sha(b'changed');dump(self.source/'CML3111_W03_manifest.json',meta)
        kept,todo=runner.select_work(self.source,raw,[self.old_grade]);self.assertFalse(kept);self.assertEqual(len(todo),1)

    def test_merge_omitted_attempts_and_reject_identity_rewrite(self):
        incoming=self.root/'new';(incoming/'files').mkdir(parents=True)
        (incoming/'files/file2.bin').write_bytes(b'second')
        fresh=manifest([receipt('two','file2')],b'second','file2');fresh['exported_at']='2026-10-21T00:00:00Z'
        dump(incoming/'CML3111_W03_manifest.json',fresh)
        out=self.root/'merged';runner.merge_sources(self.source,incoming,out)
        self.assertEqual(len(runner.read(out/'CML3111_W03_manifest.json')['records']),2)
        runner.merge_sources(self.source,incoming,out)
        self.assertEqual(len(runner.read(out/'CML3111_W03_manifest.json')['records']),2)
        changed=receipt();changed['email']='different@example.test'
        dump(incoming/'CML3111_W03_manifest.json',manifest([changed]))
        with self.assertRaisesRegex(ValueError,'identity'):runner.merge_sources(self.source,incoming,self.root/'conflict')

    def batch(self,name='download',rid='two'):
        d=self.root/name;d.mkdir()
        for c in runner.COHORTS:(d/f'{c}_quiz_source.xlsx').write_bytes(b'workbook fixture')
        (d/'assignment_source.xlsx').write_bytes(b'audit fixture')
        with zipfile.ZipFile(d/'export.zip','w') as z:z.writestr('marker',rid)
        return d

    def prepared(self,download,batch,previous):
        incoming=batch/'fresh';(incoming/'files').mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(Path(download)/'export.zip') as z:rid=z.read('marker').decode()
        (incoming/'files/file2.bin').write_bytes(b'second')
        r=receipt(rid,'file2');r['submitted_at']='2026-10-02T09:00:00Z'
        dump(incoming/'CML3111_W03_manifest.json',manifest([r],b'second','file2'))
        runner.merge_sources(previous/'reconciled',incoming,batch/'reconciled')
        dump(batch/'reconciled/timing.json',{})

    def fake_grade(self,batch,todo):
        self.assertEqual(len(todo),1)
        r=todo[0]
        return [dict(cohort=r['cohort'],assessment=r['assessment'],student_id=r['student_id'],response_id=r['response_id'],score=19,status='GRADED',source_hashes={'file2':sha(b'second')})]

    def fake_render(self,batch):(batch/runner.BOOK).write_bytes(b'new workbook')

    def test_end_to_end_rerun_no_duplicates_and_history_preserved(self):
        download=self.batch()
        with patch.object(runner,'prepare_batch',side_effect=self.prepared):
            first=runner.refresh(download,self.private,grader=self.fake_grade,renderer=self.fake_render)
            second=runner.refresh(download,self.private,grader=lambda *x:self.fail('Repeated grading'),renderer=lambda *x:self.fail('Repeated render'))
        self.assertEqual(first,second);self.assertEqual(first['new_receipts'],1)
        ledger=runner.read(self.private/'ledger.json')
        self.assertEqual([x['score'] for x in ledger['attempts']],[17,19]);self.assertEqual(ledger['current'][0]['score'],19)
        self.assertEqual((self.private/'before_one_command'/runner.BOOK).read_bytes(),b'original workbook')

    def test_failure_keeps_workbook_and_resume_uses_same_batch(self):
        download=self.batch()
        with patch.object(runner,'prepare_batch',side_effect=self.prepared):
            with self.assertRaisesRegex(RuntimeError,'simulated'):
                runner.refresh(download,self.private,grader=self.fake_grade,renderer=lambda b:(_ for _ in ()).throw(RuntimeError('simulated renderer failure')))
            self.assertEqual((self.private/runner.BOOK).read_bytes(),b'original workbook')
            runner.refresh(download,self.private,grader=self.fake_grade,renderer=self.fake_render)
        self.assertEqual(len(runner.read(self.private/'ledger.json')['attempts']),2)

    def test_publication_crash_recovers_and_lock_blocks_second_writer(self):
        batch=self.private/'batches/test';batch.mkdir(parents=True)
        dump(batch/'ledger.json',{'attempts':[]});(batch/runner.BOOK).write_bytes(b'complete');dump(batch/'status.json',{'state':'COMPLETE'});dump(batch/'summary.json',{})
        dump(self.private/'refresh_publish.json',{'generation':'batches/test'})
        runner.finish_publish(self.private);self.assertEqual((self.private/runner.BOOK).read_bytes(),b'complete')
        with runner.exclusive(self.private):
            with self.assertRaisesRegex(RuntimeError,'already running'):
                with runner.exclusive(self.private):pass

    def test_test_and_project_marks_retained(self):
        extras=[]
        for assessment in ['TEST1','ML_PROJECT']:
            extras.append(dict(cohort='CML3111',assessment=assessment,student_id='SYNTHETIC-ONLY',submitted_student_id='SYNTHETIC-ONLY',email='synthetic@example.test',full_name='Synthetic',response_id=assessment,submitted_at='2026-10-10T09:00:00Z',timing_status='ON_TIME',status='GRADED',score=80,source_score=80,source_status='GRADED',maximum=100,file_ids=[],source='production.json'))
        result=ca.build(self.source,self.private/'written_queue/combined_results.json',retained_attempts=extras)
        self.assertEqual({r['assessment']:r['score'] for r in result['current']},{'W03':17,'TEST1':80,'ML_PROJECT':80})

    def test_older_export_cannot_replace_newer_snapshot(self):
        incoming=self.root/'stale';(incoming/'files').mkdir(parents=True)
        (incoming/'files/file1.bin').write_bytes(self.data)
        m=manifest([receipt()]);m['exported_at']='2026-10-19T00:00:00Z'
        dump(incoming/'CML3111_W03_manifest.json',m)
        with self.assertRaisesRegex(ValueError,'older'):
            runner.merge_sources(self.source,incoming,self.root/'merged')

    def test_external_ledger_changes_are_not_overwritten(self):
        download=self.batch()
        with patch.object(runner,'prepare_batch',side_effect=self.prepared):
            runner.refresh(download,self.private,grader=self.fake_grade,renderer=self.fake_render)
        ledger=runner.read(self.private/'ledger.json');ledger['external_change']=True;dump(self.private/'ledger.json',ledger)
        with self.assertRaisesRegex(ValueError,'outside this runner'):runner.active_base(self.private)
        self.assertTrue(runner.read(self.private/'ledger.json')['external_change'])

    def test_missing_downloads_stop_before_grading(self):
        d=self.root/'empty';d.mkdir()
        with self.assertRaisesRegex(ValueError,'Missing downloads'):runner.refresh(d,self.private)
        self.assertEqual((self.private/runner.BOOK).read_bytes(),b'original workbook')

    def test_real_zip_excel_import_and_ledger_merge(self):
        import io
        d=self.root/'real';d.mkdir()
        deadlines={f'{c}|{i}':{'closeAt':1793404800000} for c in runner.COHORTS for i in range(1,6)}
        dump(self.private/'quiz_deadlines.json',deadlines)
        old=receipt();new=receipt('two','file2');new['submitted_at']='2026-10-02T09:00:00Z'
        with zipfile.ZipFile(d/'export.zip','w') as z:
            for c in runner.COHORTS:
                for i in range(1,6):
                    m=manifest([]);m.update(key=f'{c}|W{i:02}',files=[])
                    if c=='CML3111' and i==3:
                        m=manifest([old,new]);m['files'].append(dict(id='file2',sha256=sha(b'second'),export_name='file2.bin'))
                        buf=io.BytesIO()
                        with zipfile.ZipFile(buf,'w') as inner:
                            inner.writestr('file1.bin',b'first');inner.writestr('file2.bin',b'second')
                        z.writestr('CML3111_W03_files_1.zip',buf.getvalue())
                    z.writestr(f'{c}_W{i:02}_manifest.json',json.dumps(m))
                    q=dict(key=f'{c}|{i}',items=[dict(id='q',points=5)],records=[])
                    if c=='CML3111' and i==1:q['records']=[dict(response_id='quiz-one',email='synthetic@example.test',submitted_at='2026-10-01T09:00:00Z',answers=[dict(id='reg',title='Student Registration Number',answer='SYNTHETIC-ONLY')])]
                    z.writestr(f'{c}_Q{i}_quiz.json',json.dumps(dict(exported_at='2026-10-20T00:00:00Z',quizzes=[q])))
        headers=['response_id','assessment_key','student_id','email','submitted_at','status','file_ids']
        rows=[headers]+[[r['response_id'],r['assessment_key'],'SYNTHETIC-ONLY',r['email'],r['submitted_at'],'ON_TIME',json.dumps(r['file_ids'])] for r in [old,new]]
        xlsx(d/'assignment_source.xlsx',{'Submission audit':rows})
        from datetime import datetime
        serial=(datetime(2026,10,1,12)-datetime(1899,12,30)).total_seconds()/86400
        for c in runner.COHORTS:
            sheets={f'Form Responses {i}':[['Timestamp','Email Address','Score','Student Registration Number']] for i in range(1,6)}
            if c=='CML3111':sheets['Form Responses 1'].append([(serial,),'synthetic@example.test',4,'SYNTHETIC-ONLY'])
            xlsx(d/f'{c}_quiz_source.xlsx',sheets)
        runner.refresh(d,self.private,grader=self.fake_grade,renderer=self.fake_render)
        result=runner.read(self.private/'ledger.json')
        self.assertEqual(len(result['attempts']),3)
        self.assertEqual({r['assessment']:r['score'] for r in result['current']},{'W03':19,'Q1':4})

    def test_real_zip_incomplete_is_rejected(self):
        b=self.private/'batches/bad';(b/'downloads').mkdir(parents=True)
        with zipfile.ZipFile(b/'downloads/export.zip','w') as z:z.writestr('CML3111_W03_manifest.json',json.dumps(manifest([])))
        with self.assertRaisesRegex(ValueError,'Incomplete export'):runner.prepare_batch(b/'downloads',b,self.private)

if __name__=='__main__':unittest.main()
