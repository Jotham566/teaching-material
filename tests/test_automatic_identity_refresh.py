"""New submission evidence participates in the normal workbook refresh."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
import continuous_assessment as ca
import refresh_ca as refresh
from test_registration_reconciliation import row


class AutomaticIdentityTests(unittest.TestCase):
    def test_new_file_evidence_corrects_typo_without_separate_command(self):
        with tempfile.TemporaryDirectory() as temp:
            batch=Path(temp);source=batch/'reconciled';(source/'files').mkdir(parents=True)
            target='99/UG/987/BARC-S';original='99/UG/987/BBARC-S'
            rows=[row(original,cohort='CML3112'),row(target,'r2',cohort='CML3112',assessment='Q2',file_ids=['f2']),row(target,'r3',cohort='CML3112',assessment='Q3',file_ids=['f3'])]
            files=[]
            for number in (2,3):
                text=f'Name: Alex Smith\nRegistration: {target}\nExercise {number}'
                filename=f'f{number}.txt';(source/'files'/filename).write_text(text)
                files.append(dict(id=f'f{number}',sha256=hashlib.sha256(text.encode()).hexdigest(),export_name=filename))
            refresh.write(source/'manifest.json',{'files':files})
            ledger=ca.finalize(copy.deepcopy(rows),[])
            self.assertTrue(any(r['status']=='IDENTITY_CONFLICT' for r in ledger['current']))
            with patch.object(refresh,'ensure_docker',side_effect=AssertionError('No Docker for text')),patch('recover_student_names.extract_name',side_effect=AssertionError('No extra AI inference')):
                refresh.reconcile_batch_identities(ledger,batch)
                before=[(r['response_id'],r['student_id'],r['score']) for r in ledger['current']]
                refresh.reconcile_batch_identities(ledger,batch)
            self.assertEqual({r['student_id'] for r in ledger['current']},{target})
            self.assertTrue(all(r['status']=='GRADED' for r in ledger['current']))
            self.assertEqual(before,[(r['response_id'],r['student_id'],r['score']) for r in ledger['current']])
            self.assertEqual(ledger['attempts'][0]['submitted_student_id'],original)
            self.assertTrue((batch/'registration_reconciliation.json').is_file())

    def test_unreadable_new_file_retains_saved_ai_name(self):
        with tempfile.TemporaryDirectory() as temp:
            previous=Path(temp)/'previous';batch=Path(temp)/'batch';previous.mkdir();batch.mkdir()
            source=batch/'reconciled';source.mkdir()
            r=row('99/UG/987/BARC-S',cohort='CML3112',file_ids=['file'])
            saved={'r1':[dict(file_id='file',sha256='hash',name='Alex Smith',quote='Alex Smith',header='Alex Smith',method='saved local AI',registrations=[])]}
            refresh.write(previous/'identity_evidence.json',saved)
            refresh.write(source/'manifest.json',{'files':[dict(id='file',sha256='hash',export_name='missing.pdf')]})
            refresh.seed_identity_cache(previous,batch)
            ledger=ca.finalize([r],[]);refresh.reconcile_batch_identities(ledger,batch)
            ev=refresh.read(batch/'identity_evidence.json')['r1'][0]
            self.assertEqual(ev['name'],'Alex Smith');self.assertTrue(ev['error'])
            self.assertEqual(len(ledger['attempts']),1)


if __name__=='__main__':unittest.main()
