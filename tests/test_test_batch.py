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
if __name__=='__main__':unittest.main()
