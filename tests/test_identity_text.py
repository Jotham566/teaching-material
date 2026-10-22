import json,sys,tempfile,hashlib
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'IUEA_Teaching_Plan/grader'))
from identity_text import names,registrations,prepare
from recover_student_names import collect,compatible_name_keys
from test_registration_reconciliation import RegistrationTests,row

class TextTests(unittest.TestCase):
 def test_omitted_name_part_is_not_a_conflict(self):
  self.assertTrue(compatible_name_keys({'alex smith','alex john smith'}))
  self.assertFalse(compatible_name_keys({'alex james smith','alex john smith'}))
  self.assertFalse(compatible_name_keys({'alex','alex smith'}))
 def test_common_name_layouts(self):
  for text in ('**Name:** Alex Smith','| Name | Alex Smith |','NAME\nAlex Smith','student_name = "Alex Smith"','Name: Alex Smith REG: 99/987/BSPE-S'):
   self.assertEqual(names(text)[0]['name'],'Alex Smith',text)
 def test_registrations_are_quoted_not_guessed(self):
  self.assertEqual(registrations('STUDENT_ID = "99_UG_987_BSPE_S"')[0]['registration'],'99/UG/987/BSPE-S')
  text='Registration: 99 / UG / 987 / BSPE=S'
  r=registrations(text)[0];self.assertEqual(r['registration'],'99/UG/987/BSPE-S');self.assertIn(r['quote'],text)
 def test_document_uses_original_unredacted_extractor(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);source=base/'reconciled';(source/'files').mkdir(parents=True);out=base/'out';out.mkdir()
   f=source/'files/a.docx';f.write_bytes(b'synthetic');sha=hashlib.sha256(f.read_bytes()).hexdigest()
   (source/'manifest.json').write_text(json.dumps({'files':[dict(id='f',sha256=sha,export_name='a.docx')]}))
   ledger={'attempts':[row('99/987/BSPE-S',file_ids=['f'])]}
   with patch('refresh_ca.ensure_docker'),patch('render_submission.extract_document',return_value='Name: Alex Smith\nRegistration: 99/987/BSPE-S') as extract:
    cache=prepare(ledger,base,out);self.assertIn('99/987/BSPE-S',cache[sha]['text']);extract.assert_called_once_with(f)
   ev=collect(ledger,base,out,'',False)
   self.assertEqual(ev['r1'][0]['registrations'][0]['registration'],'99/987/BSPE-S')

class AccountTests(RegistrationTests):
 def test_two_accounts_need_distinct_files_same_name_and_number(self):
  rows=[row('99/987/BSPE-S','r2',file_ids=['f0']),row('99/987/BSPE-S','r3',email='second@example.test',file_ids=['f1'],assessment='Q2')]
  e=self.evidence()
  for pp in e.values():pp[0]['registrations']=[{'registration':'99/987/BSPE-S','quote':'99/987/BSPE-S'}]
  data=self.run_rows(rows,e)
  self.assertTrue(all(r['status']=='GRADED' for r in data['current']))
  e['r3'][0]['name']='Jane Jones'
  self.assertTrue(all(r['status']=='IDENTITY_CONFLICT' for r in self.run_rows(rows,e)['current']))
 def test_same_copy_across_accounts_is_not_corroboration(self):
  rows=[row('99/987/BSPE-S','r2',file_ids=['f0']),row('99/987/BSPE-S','r3',email='second@example.test',file_ids=['f0'],assessment='Q2')]
  e=self.evidence();e['r3']=e['r2']
  for pp in e.values():pp[0]['registrations']=[{'registration':'99/987/BSPE-S'}]
  self.assertTrue(all(r['status']=='IDENTITY_CONFLICT' for r in self.run_rows(rows,e)['current']))

if __name__=='__main__':unittest.main()
