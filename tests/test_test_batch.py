import hashlib,json,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'IUEA_Teaching_Plan/grader'))
import grade_test_batch as batch
class BatchTests(unittest.TestCase):
 def run_batch(self,jobs,files):
  temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);base=Path(temp.name);archive=base/'batch.zip'
  with zipfile.ZipFile(archive,'w') as z:
   z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=jobs)))
   for name,content in files.items():z.writestr(name,content)
  with patch.object(batch,'preflight'):
   out=batch.grade_batch(archive,base/'results')
  return json.loads((out/'workbook_data.json').read_text())
 def test_unsafe_name_never_extracted(self):
  r=self.run_batch([dict(response_id='a',file='../escape.ipynb')],{'../escape.ipynb':'{}'})
  self.assertEqual(r['collection_issues'][0][10],'BATCH_ERROR');self.assertEqual(r['current'],[])
 def test_tampered_bytes_rejected(self):
  r=self.run_batch([dict(response_id='a',file='a.ipynb',notebook_sha256='0'*64)],{'a.ipynb':'{}'})
  self.assertIn('checksum',r['collection_issues'][0][14]);self.assertEqual(r['current'],[])
 def test_duplicate_response_ids_fail(self):
  with self.assertRaisesRegex(ValueError,'Duplicate response'):
   self.run_batch([dict(response_id='a'),dict(response_id='a')],{})
 def test_invalid_job_does_not_stop_next_job(self):
  content=b'{}';good=dict(response_id='b',file='b.ipynb',notebook_sha256=hashlib.sha256(content).hexdigest(),cohort='CML3111',assessment='TEST1')
  with patch.object(batch,'process',return_value={'status':'GRADED'}) as process:
   r=self.run_batch([dict(response_id='a',file='../bad.ipynb'),good],{'b.ipynb':content})
  self.assertEqual(process.call_count,1);self.assertEqual(len(r['collection_issues']),1)
 def test_incremental_issue_history_is_persistent_and_idempotent(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);out=base/'results';archives=[]
   first=['receipt','CML3113','TEST1']+['']*7+['COLLECTION_ERROR']+['']*4
   revised=first.copy();revised[14]='Different recorded reason'
   for index,issues in enumerate(([first],[],[first,revised])):
    archive=base/f'{index}.zip';archives.append(archive)
    with zipfile.ZipFile(archive,'w') as z:z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=[],collection_issues=issues)))
   with patch.object(batch,'preflight'):
    for archive in archives:batch.grade_batch(archive,out)
    batch.grade_batch(archives[-1],out)
   self.assertEqual(json.loads((out/'collection_issues.json').read_text()),[first,revised])
   self.assertEqual(json.loads((out/'workbook_data.json').read_text())['collection_issues'],[first,revised])
 def test_imports_both_legacy_issue_files_before_export(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);out=base/'results';out.mkdir()
   first=['one','CML3113','TEST1']+['']*7+['COLLECTION_ERROR']+['']*4
   second=['two','CML3113','TEST1']+['']*7+['COLLECTION_ERROR']+['']*4
   (out/'collection_issues.json').write_text(json.dumps([first]))
   (out/'workbook_data.json').write_text(json.dumps(dict(collection_issues=[second])))
   archive=base/'empty.zip'
   with zipfile.ZipFile(archive,'w') as z:z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=[])))
   with patch.object(batch,'preflight'):batch.grade_batch(archive,out)
   self.assertEqual(json.loads((out/'workbook_data.json').read_text())['collection_issues'],[first,second])
 def test_invalid_issue_data_fails_before_grading_or_overwriting(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);out=base/'results';out.mkdir()
   (out/'collection_issues.json').write_text('["invalid"]')
   archive=base/'empty.zip'
   with zipfile.ZipFile(archive,'w') as z:z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=[])))
   with patch.object(batch,'preflight'),patch.object(batch,'process') as process:
    with self.assertRaisesRegex(ValueError,'expected 15 columns'):batch.grade_batch(archive,out)
   process.assert_not_called()
   self.assertEqual((out/'collection_issues.json').read_text(),'["invalid"]')
 def test_batch_error_survives_later_successful_export(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);out=base/'results';bad=base/'bad.zip';empty=base/'empty.zip'
   with zipfile.ZipFile(bad,'w') as z:z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=[dict(response_id='a',file='../bad.ipynb')])))
   with zipfile.ZipFile(empty,'w') as z:z.writestr('manifest.json',json.dumps(dict(schema=1,jobs=[])))
   with patch.object(batch,'preflight'):
    batch.grade_batch(bad,out);batch.grade_batch(empty,out)
   issues=json.loads((out/'workbook_data.json').read_text())['collection_issues']
   self.assertEqual(len(issues),1);self.assertEqual(issues[0][10],'BATCH_ERROR')
if __name__=='__main__':unittest.main()
