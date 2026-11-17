import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

spec = importlib.util.spec_from_file_location('links', Path(__file__).resolve().parents[1] / 'scripts/attach_xlsx_hyperlinks.py')
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)


class ReviewLinksTest(unittest.TestCase):
    def test_native_link_preserves_cells_and_table_relationship(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'marks.xlsx'
            sheet = f'<worksheet xmlns="{links.MAIN}"><sheetData><row r="7"><c r="Q7" t="inlineStr"><is><t>Report.pdf</t></is></c></row></sheetData><pageMargins left="1"/><tableParts/></worksheet>'
            relation = f'<Relationships xmlns="{links.REL}"><Relationship Id="rId1" Type="table" Target="../tables/table1.xml"/></Relationships>'
            with zipfile.ZipFile(target, 'w') as z:
                z.writestr('xl/worksheets/sheet4.xml', sheet)
                z.writestr('xl/worksheets/_rels/sheet4.xml.rels', relation)
                z.writestr('other', b'preserve')
            url = 'https://drive.google.com/file/d/synthetic-file/view'
            links.attach(target, 'xl/worksheets/sheet4.xml', [('Q7', url)])
            with zipfile.ZipFile(target) as z:
                root = ET.fromstring(z.read('xl/worksheets/sheet4.xml'))
                rels = ET.fromstring(z.read('xl/worksheets/_rels/sheet4.xml.rels'))
                self.assertEqual(z.read('other'), b'preserve')
            self.assertEqual(root.find(f'.//{{{links.MAIN}}}t').text, 'Report.pdf')
            self.assertEqual(root.find(f'{{{links.MAIN}}}hyperlinks')[0].get('ref'), 'Q7')
            self.assertEqual(rels[0].get('Id'), 'rId1')
            self.assertEqual(rels[1].get('Target'), url)
            self.assertEqual(rels[1].get('TargetMode'), 'External')
            self.assertEqual([x.tag.split('}')[-1] for x in root], ['sheetData', 'hyperlinks', 'pageMargins', 'tableParts'])
