import copy
import json
import unittest
from test_registration_reconciliation import RegistrationTests, row
from reconcile_registrations import reconcile, supported_typo_kind
import continuous_assessment as ca


class ProgrammeTests(RegistrationTests):
    def scenario(self, original, target, name='Alex Smith', own_declaration=False):
        rows=[row(original,cohort='CML3112',full_name=name,file_ids=['f0'] if own_declaration else []),
              row(target,'r2',cohort='CML3112',full_name=name,assessment='W02',file_ids=['f1']),
              row(target,'r3',cohort='CML3112',full_name=name,assessment='W03',file_ids=['f2'])]
        files=[{'id':f'f{i}','sha256':str(i)} for i in range(3)]
        (self.source/'manifest.json').write_text(json.dumps({'files':files}))
        evidence={r['response_id']:[{'file_id':fid,'sha256':fid[-1],'name':name,'registrations':[{'registration':target}]} for fid in r['file_ids']] for r in rows}
        return rows,evidence

    def test_duplicate_degree_letter(self):
        rows,ev=self.scenario('99/UG/987/BBARC-J','99/UG/987/BARC-J')
        ledger=self.run_rows(rows,ev)
        self.assertEqual(len(ledger['students']),1)
        self.assertTrue(all(r['status']=='GRADED' for r in ledger['current']))
        before=copy.deepcopy(ledger['current']);reconcile(ledger,ev,self.source)
        self.assertEqual([(r['student_id'],r['score']) for r in before],[(r['student_id'],r['score']) for r in ledger['current']])

    def test_ig_and_repeated_e(self):
        for raw,target in [('99/IG/987/BARC-S','99/UG/987/BARC-S'),('99/987/BSCEE-S','99/987/BSCE-S')]:
            rows,ev=self.scenario(raw,target)
            self.assertEqual(len(self.run_rows(rows,ev)['students']),1)

    def test_incomplete_year_requires_same_receipt_declaration(self):
        for own in (False,True):
            rows,ev=self.scenario('9/UG/987/BARC-S','99/UG/987/BARC-S',name='',own_declaration=own)
            self.assertEqual(len(self.run_rows(rows,ev)['students']),1 if own else 2)

    def test_conflicting_names_stale_files_and_other_account_block(self):
        for problem in ('name','hash','account'):
            rows,ev=self.scenario('99/UG/987/BBARC-J','99/UG/987/BARC-J')
            if problem=='name':rows[0]['full_name']='Jane Jones'
            if problem=='hash':ev['r2'][0]['sha256']='bad'
            if problem=='account':rows.append(row('99/UG/987/BARC-J','r4',cohort='CML3112',email='other@example.test'))
            self.assertEqual(len(self.run_rows(rows,ev)['students']),2)

    def test_serial_suffix_and_wrong_programme_are_not_candidates(self):
        for raw,target,course in [('99/987/BSC-E','99/987/BSCE-S','CML3112'),('99/988/BBARC-J','99/987/BARC-J','CML3112'),('99/987/BBARC-J','99/987/BARC-J','CML3113'),('98/987/BARC-J','99/987/BARC-J','CML3112')]:
            self.assertEqual(supported_typo_kind(raw,target,course),'')

    def test_separator_only_does_not_apply_programme_changes(self):
        rows,ev=self.scenario('99/UG/987/BBARC-J','99/UG/987/BARC-J')
        ledger=ca.finalize(rows,[]);reconcile(ledger,ev,self.source,separator_only=True)
        self.assertEqual(len(ledger['students']),2)


if __name__=='__main__':unittest.main()
