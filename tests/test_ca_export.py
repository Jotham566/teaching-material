import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from unpack_ca_export import unpack


class ExportTests(unittest.TestCase):
    def test_nested_attachment_verified_and_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            content=b'{"cells":[]}'
            inner=io.BytesIO()
            with zipfile.ZipFile(inner,'w') as z:
                z.writestr('fixture.ipynb',content)
            meta=dict(files=[dict(id='fixture',export_name='fixture.ipynb',
                                 sha256=hashlib.sha256(content).hexdigest())],errors=[])
            archive=root/'download.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('Drive folder/CML3111_W03_files_1.zip',inner.getvalue())
                z.writestr('Drive folder/CML3111_W03_manifest.json',json.dumps(meta))
            self.assertEqual(unpack(archive,root/'out'),(1,[]))
            self.assertEqual(unpack(archive,root/'out'),(1,[]))

    def test_path_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            archive=root/'bad.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('../outside.json','{}')
            with self.assertRaisesRegex(ValueError,'Unsafe'):
                unpack(archive,root/'out')
            self.assertFalse((root/'outside.json').exists())

    def test_tampered_attachment_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            inner=io.BytesIO()
            with zipfile.ZipFile(inner,'w') as z:z.writestr('fixture.ipynb',b'changed')
            archive=root/'download.zip'
            with zipfile.ZipFile(archive,'w') as z:
                z.writestr('CML3111_W03_files_1.zip',inner.getvalue())
                z.writestr('CML3111_W03_manifest.json',json.dumps(dict(files=[
                    dict(id='fixture',export_name='fixture.ipynb',sha256='0'*64)],errors=[])))
            with self.assertRaisesRegex(ValueError,'checksum'):
                unpack(archive,root/'out')


if __name__=='__main__':unittest.main()
