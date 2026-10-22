import copy
import sys
from pathlib import Path
import unittest
import io,json,tempfile
from unittest.mock import patch
import recover_student_names as names
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from recover_student_names import apply_evidence, labelled_names, email_support, valid_name

def ledger():
    row=dict(response_id='r1',cohort='CML3111',student_id='DEMO/BSCE-A',submitted_student_id='DEMO/BSCE-A',email='alex.smith@example.test',full_name='',status='GRADED',score=16,assessment='W03')
    return {'attempts':[row],'current':[dict(row)],'students':[{'cohort':row['cohort'],'student_id':row['student_id'],'full_name':''}]}

def proposal(name='Alex Smith',sha='one'):
    return dict(name=name,quote='Student name: '+name,method='explicit name label',sha256=sha,header='Student name: '+name+'\nRegistration: DEMO/BSCE-A')

class NamesTests(unittest.TestCase):
    def test_confirmed_name_fills_without_touching_marks(self):
        data=ledger();apply_evidence(data,{'r1':[proposal()]})
        self.assertEqual(data['students'][0]['full_name'],'Alex Smith')
        self.assertEqual(data['attempts'][0]['score'],16)
        self.assertEqual(data['attempts'][0]['student_id'],'DEMO/BSCE-A')
    def test_email_alone_never_creates_name(self):
        data=ledger();apply_evidence(data,{})
        self.assertEqual(data['students'][0]['full_name'],'')
    def test_unsupported_or_conflicting_name_is_reviewed(self):
        for evidence in ([proposal('Mary Jones')],[proposal(),proposal('Mary Jones','two')]):
            data=ledger();apply_evidence(data,{'r1':evidence})
            self.assertEqual(data['students'][0]['full_name'],'')
            self.assertEqual(data['identity_review'][0]['status'],'REVIEW')
    def test_repeated_copy_is_not_independent_support(self):
        data=ledger();data['attempts'][0]['email']='account@example.test'
        apply_evidence(data,{'r1':[proposal(),proposal()]})
        self.assertEqual(data['attempts'][0]['full_name'],'')
    def test_identity_conflict_never_released(self):
        data=ledger();data['attempts'][0]['status']='IDENTITY_CONFLICT'
        apply_evidence(data,{'r1':[proposal()]})
        self.assertEqual(data['attempts'][0]['full_name'],'')
        self.assertEqual(data['attempts'][0]['status'],'IDENTITY_CONFLICT')
    def test_mixed_degree_codes_preserved(self):
        data=ledger();other=dict(data['attempts'][0],response_id='r2',student_id='DEMO/BSME-A',submitted_student_id='DEMO/BSME-A')
        data['attempts'].append(other);apply_evidence(data,{})
        self.assertEqual(other['student_id'],'DEMO/BSME-A')
        self.assertIn('DEMO/BSME-A',data['identity_review'][0]['cohort_formats'])
    def test_ai_cannot_invent_unquoted_name(self):
        payload={'message':{'content':json.dumps({'name':'Alex Smith','quote':'Made up quotation'})}}
        with patch.object(names.artifact_grade.LOCAL_HTTP,'open',return_value=io.BytesIO(json.dumps(payload).encode())):
            with self.assertRaisesRegex(ValueError,'exact quotation'):
                names.extract_name('A document with no author named here.','local-test-model')

    def test_changed_attachment_does_not_reuse_old_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp);data=ledger();data['attempts'][0]['source']='manifest.json'
            (source/'manifest.json').write_text(json.dumps({'files':[{'id':'file','sha256':'new'}]}))
            evidence=proposal();evidence['file_id']='file'
            apply_evidence(data,{'r1':[evidence]},source)
            self.assertEqual(data['students'][0]['full_name'],'')

    def test_labels_and_email_are_conservative(self):
        self.assertEqual(labelled_names('Student name: Alex Smith')[0]['name'],'Alex Smith')
        self.assertFalse(valid_name('Your Name'));self.assertFalse(valid_name('Alex Smith 123'))
        self.assertFalse(email_support('Alex Smith','alex@example.test'))

if __name__=='__main__':unittest.main()
