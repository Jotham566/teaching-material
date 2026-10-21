import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from recover_ca_file_extensions import recover

class FormatRecoveryTests(unittest.TestCase):
 def test_notebook_extension_recovery_preserves_uploaded_bytes(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder);(p/'files').mkdir();content=b'{"nbformat":4,"cells":[]}'
   (p/'files/f.txt').write_bytes(content);sha=hashlib.sha256(content).hexdigest()
   (p/'test_manifest.json').write_text(json.dumps({'files':[{'id':'f','export_name':'f.txt','original_name':'example.txt','sha256':sha}]}))
   changes=recover(p);self.assertEqual(len(changes),1)
   self.assertEqual((p/'files/f.ipynb').read_bytes(),content)
   self.assertEqual((p/'files/f.txt').read_bytes(),content)
   meta=json.loads((p/'test_manifest.json').read_text())['files'][0]
   self.assertEqual(meta['sha256'],sha);self.assertEqual(meta['original_export_name'],'f.txt')
   self.assertEqual(recover(p),[])

if __name__=='__main__':unittest.main()
