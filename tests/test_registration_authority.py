import hashlib,json,tempfile,unittest
from pathlib import Path
from test_registration_reconciliation import row
import continuous_assessment as ca
from reconcile_registrations import reconcile

class RegistrationAuthorityTests(unittest.TestCase):
    def test_registration_groups_accounts_without_name_or_email(self):
        with tempfile.TemporaryDirectory() as temp:
            rows=[row('99/987/BARC-S',cohort='CML3112',full_name=''),row('99/987/BARC-S','r2',cohort='CML3112',email='other@example.test',assessment='Q2',full_name=''),row('99/987/BARC-S','r3',cohort='CML3112',email='',assessment='Q3',full_name='')]
            ledger=ca.finalize(rows,[]);reconcile(ledger,{},Path(temp)/'reconciled')
            self.assertEqual(len(ledger['students']),1)
            self.assertTrue(all(r['score']==4 for r in ledger['current']))

    def test_confirmed_alias_and_name_with_private_policy(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);source=base/'reconciled';source.mkdir()
            policy={'approved_aliases':{'CML3112':{'99/987/BSEC-S':'99/987/BSCE-S'}},'confirmed_names':{'CML3112':{'99/987/BSCE-S':'CONFIRMEDNAME'}}}
            (base/'identity_policy.json').write_text(json.dumps(policy))
            ledger=ca.finalize([row('99/987/BSEC-S',cohort='CML3112',full_name='')],[]);reconcile(ledger,{},source)
            self.assertEqual(ledger['current'][0]['student_id'],'99/987/BSCE-S');self.assertEqual(ledger['students'][0]['full_name'],'CONFIRMEDNAME')

    def test_notebook_precedence_requires_original_file_and_grade_hash(self):
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp);source=base/'reconciled';(source/'files').mkdir(parents=True);(base/'written_queue').mkdir()
            content=b'{}';(source/'files/n.ipynb').write_bytes(content);sha=hashlib.sha256(content).hexdigest()
            (source/'manifest.json').write_text(json.dumps({'files':[{'id':'f','sha256':sha,'export_name':'n.ipynb'}]}))
            g={'response_id':'r1','student_id':'99/111/BARC-S','cohort':'CML3112','assessment':'W03','source_hashes':{'f':sha},'record':{'declared_sid':'99/222/BARC-S','questions':{'q':{'marks':20,'awarded':18}}}}
            (base/'written_queue/combined_results.json').write_text(json.dumps([g]))
            for valid in (True,False):
                if not valid:(source/'files/n.ipynb').write_text('changed')
                ledger=ca.finalize([row('99/111/BARC-S',cohort='CML3112',assessment='W03',status='IDENTITY_MISMATCH',score=None,file_ids=['f'])],[])
                reconcile(ledger,{},source)
                self.assertEqual(ledger['current'][0]['student_id'],'99/222/BARC-S' if valid else '99/111/BARC-S')
                self.assertEqual(ledger['current'][0]['score'],18 if valid else None)
                self.assertEqual(ledger['attempts'][0]['submitted_student_id'],'99/111/BARC-S')

if __name__=='__main__':unittest.main()
