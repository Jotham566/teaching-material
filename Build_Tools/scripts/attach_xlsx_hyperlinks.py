"""Add native Excel links after export (the authoring engine cannot calculate HYPERLINK)."""
import json
import os
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

MAIN = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
DOCREL = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'

def attach(filename, sheet_part, links):
    filename = Path(filename)
    ET.register_namespace('', MAIN)
    ET.register_namespace('r', DOCREL)
    with zipfile.ZipFile(filename) as source:
        entries = {name: source.read(name) for name in source.namelist()}
    root = ET.fromstring(entries[sheet_part])
    rel_part = str(Path(sheet_part).parent / '_rels' / (Path(sheet_part).name + '.rels'))
    rels = ET.fromstring(entries[rel_part]) if rel_part in entries else ET.Element(f'{{{REL}}}Relationships')
    existing = {x.attrib['Id'] for x in rels}
    node = root.find(f'{{{MAIN}}}hyperlinks')
    if node is None:
        node = ET.Element(f'{{{MAIN}}}hyperlinks')
        # OOXML requires hyperlinks after validations and before print settings.
        later = {'printOptions', 'pageMargins', 'pageSetup', 'headerFooter', 'rowBreaks', 'colBreaks',
                 'customProperties', 'cellWatches', 'ignoredErrors', 'smartTags', 'drawing',
                 'legacyDrawing', 'legacyDrawingHF', 'picture', 'oleObjects', 'controls',
                 'webPublishItems', 'tableParts', 'extLst'}
        position = next((i for i, x in enumerate(root) if x.tag.split('}')[-1] in later), len(root))
        root.insert(position, node)
    for i, (cell, url) in enumerate(links, 1):
        if not url.startswith('https://drive.google.com/file/d/') and not url.startswith('https://docs.google.com/forms/d/'):
            raise ValueError('Unexpected review URL')
        rid = f'caReviewLink{i}'
        if rid in existing:
            raise ValueError('Links already attached')
        ET.SubElement(rels, f'{{{REL}}}Relationship', Id=rid, Type=DOCREL+'/hyperlink', Target=url, TargetMode='External')
        ET.SubElement(node, f'{{{MAIN}}}hyperlink', {'ref': cell, f'{{{DOCREL}}}id': rid})
    entries[sheet_part] = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    entries[rel_part] = ET.tostring(rels, encoding='utf-8', xml_declaration=True)
    handle, temporary = tempfile.mkstemp(dir=filename.parent, suffix='.xlsx')
    os.close(handle)
    try:
        with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED) as target:
            for name, content in entries.items():
                target.writestr(name, content)
        os.replace(temporary, filename)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)

if __name__ == '__main__':
    # File input avoids large synchronous stdin pipes blocking on macOS.
    if len(sys.argv) == 4:
        with open(sys.argv[3], encoding='utf-8') as stream:
            links = json.load(stream)
    else:
        links = json.load(sys.stdin)
    attach(sys.argv[1], sys.argv[2], links)
