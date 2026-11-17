"""Large hyperlink batches must not depend on a synchronous stdin pipe."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree as ET

class HyperlinkFileTests(unittest.TestCase):
    def test_large_file_input_with_closed_stdin(self):
        script=Path(__file__).resolve().parents[1]/'scripts/attach_xlsx_hyperlinks.py'
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);book=root/'marks.xlsx';links=root/'links.json'
            part='xl/worksheets/sheet9.xml'
            with zipfile.ZipFile(book,'w') as z:
                z.writestr(part,'<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData/></worksheet>')
            rows=[[f'N{i+7}',f'https://drive.google.com/file/d/synthetic_{i}/view'] for i in range(10000)]
            links.write_text(json.dumps(rows))
            self.assertGreater(links.stat().st_size,65536)
            subprocess.run([sys.executable,str(script),str(book),part,str(links)],stdin=subprocess.DEVNULL,check=True,timeout=20)
            with zipfile.ZipFile(book) as z:
                rels=ET.fromstring(z.read('xl/worksheets/_rels/sheet9.xml.rels'))
                self.assertEqual(len(rels),10000)
                self.assertEqual(rels[-1].get('Target'),rows[-1][1])
                self.assertIsNone(z.testzip())

if __name__=='__main__':unittest.main()
