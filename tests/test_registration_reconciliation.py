import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import continuous_assessment as ca
from reconcile_registrations import canonical,reconcile
from recover_student_names import apply_evidence


def row(sid, rid='r1', **kwargs):
    result=dict(cohort='CML3111',student_id=sid,submitted_student_id=sid,email='alex.smith@example.test',
        full_name='Alex Smith',assessment='Q1',response_id=rid,submitted_at='2026-09-01T10:00:00Z',
        timing_status='ON_TIME',status='GRADED',score=4,maximum=5,file_ids=[],source='manifest.json')
    result.update(kwargs);return result

class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.source=self.root/'reconciled';self.source.mkdir()
    def tearDown(self):self.tmp.cleanup()
    def run_rows(self, rows, evidence=None):
        ledger=ca.finalize(copy.deepcopy(rows),[])
        reconcile(ledger,evidence or {},self.source)
        apply_evidence(ledger,evidence or {},self.source)
        return ledger
    def test_punctuation_and_slash_suffix(self):
        for sid in ("99/UG/987/'BSPE-J",'99/987/BSPE/S'):
            clean=canonical(sid)
            data=self.run_rows([row(sid),row(clean,'r2',assessment='Q2')])
            self.assertEqual(len(data['students']),1)
            self.assertEqual([x['score'] for x in data['current']],[4,4])
            self.assertEqual(data['attempts'][0]['submitted_student_id'],sid)
            self.assertNotIn("'",clean);self.assertIn('-',clean)
    def test_duplicate_attempt_uses_latest_not_sum(self):
        data=self.run_rows([row('99/987/BSPE/S'),row('99/987/BSPE-S','r2',score=3,submitted_at='2026-09-02T10:00:00Z')])
        self.assertEqual(len(data['attempts']),2);self.assertEqual(len(data['current']),1)
        self.assertEqual(data['current'][0]['score'],3)
    def test_repeated_pass_preserves_scores(self):
        data=self.run_rows([row('99/987/BSPE/S'),row('99/987/BSPE-S','r2',assessment='Q2')])
        old=copy.deepcopy(data['current']);reconcile(data,{},self.source)
        self.assertEqual([(r['response_id'],r['score'],r['student_id']) for r in old],[(r['response_id'],r['score'],r['student_id']) for r in data['current']])
    def test_conflicting_names_remain_held(self):
        data=self.run_rows([row('99/987/BSPE/S'),row('99/987/BSPE-S','r2',full_name='Jane Jones',assessment='Q2')])
        self.assertTrue(all(r['status']=='IDENTITY_CONFLICT' and r['score'] is None for r in data['current']))
    def test_different_programmes_and_numbers_not_guessed(self):
        data=self.run_rows([row('99/987/BSPE-S'),row('99/987/BSME-S','r2'),row('99/988/BSPE-S','r3')])
        self.assertEqual(len(data['students']),3)
        self.assertTrue(all(r['score'] is None for r in data['current']))
    def test_late_and_written_hold_preserved(self):
        data=self.run_rows([row('99/987/BSPE/S',timing_status='LATE'),row('99/987/BSPE-S','r2',assessment='W01',status='WRITTEN_REVIEW',score=None)])
        self.assertEqual([r['status'] for r in data['current']],['TIMING_REVIEW','WRITTEN_REVIEW'])
    def evidence(self):
        files=[dict(id='f'+str(i),sha256=str(i)) for i in range(2)]
        (self.source/'manifest.json').write_text(json.dumps({'files':files}))
        return {'r'+str(i+2):[dict(file_id=f['id'],sha256=f['sha256'],name='Alex Smith',header='Registration: 99/987/BSPE-S')] for i,f in enumerate(files)}
    def test_missing_letter_requires_independent_evidence(self):
        rows=[row('99/987/BSP-S'),row('99/987/BSPE-S','r2',file_ids=['f0']),row('99/987/BSPE-S','r3',file_ids=['f1'])]
        self.assertEqual(len(self.run_rows(rows)['students']),2)
        evidence=self.evidence()
        self.assertEqual(len(self.run_rows(rows,evidence)['students']),1)
        evidence['r3'][0]['sha256']='stale'
        self.assertEqual(len(self.run_rows(rows,evidence)['students']),2)
    def test_competing_account_blocks_letter_merge(self):
        rows=[row('99/987/BSP-S'),row('99/987/BSPE-S','r2',file_ids=['f0']),row('99/987/BSPE-S','r3',file_ids=['f1']),row('99/987/BSPE-S','r4',email='other@example.test')]
        self.assertEqual(len(self.run_rows(rows,self.evidence())['students']),2)
    def test_notebook_mark_release_requires_hash_and_full_questions(self):
        raw="99/987/'BSPE-S";r=row(raw,assessment='W03',status='IDENTITY_MISMATCH',score=None,maximum=20,file_ids=['f'])
        (self.source/'files').mkdir();(self.source/'files/answer.ipynb').write_text('{}')
        sha=hashlib.sha256(b'{}').hexdigest()
        (self.source/'manifest.json').write_text(json.dumps({'files':[dict(id='f',sha256=sha,export_name='answer.ipynb')]}))
        grades=self.root/'written_queue';grades.mkdir()
        g=dict(response_id='r1',cohort='CML3111',assessment='W03',student_id=raw,source_hashes={'f':sha},record={'declared_sid':'99/987/BSPE-S','questions':{'q':{'marks':20,'awarded':17}}})
        (grades/'combined_results.json').write_text(json.dumps([g]))
        self.assertEqual(self.run_rows([r])['current'][0]['score'],17)
        (self.source/'files/answer.ipynb').write_text('changed')
        self.assertEqual(self.run_rows([r])['current'][0]['status'],'IDENTITY_MISMATCH')
    def test_unknown_format_not_rewritten(self):
        self.assertEqual(canonical('ABC/12/3'), 'ABC/12/3')

if __name__=='__main__':unittest.main()
