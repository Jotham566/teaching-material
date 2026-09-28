"""Extract accessible text inside the document sandbox, never on the host."""
import json,re,subprocess,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
LIMIT=12000
source=next(Path('/input').glob('submission.*'))
def paragraphs(blob):
 root=ET.fromstring(blob)
 return [''.join(n.text or '' for n in p.iter() if n.tag.rsplit('}',1)[-1]=='t') for p in root.iter() if p.tag.rsplit('}',1)[-1]=='p']
if source.suffix=='.pdf':
 target=Path('/tmp/content.txt')
 subprocess.run(['pdftotext','-enc','UTF-8',str(source),str(target)],check=True,timeout=60,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 if target.stat().st_size>4*LIMIT:raise ValueError('Document text exceeds supported limit')
 text=target.read_text()
else:
 with zipfile.ZipFile(source) as z:
  if sum(i.file_size for i in z.infolist())>80*1024*1024:raise ValueError('Expanded document exceeds limit')
  if source.suffix=='.docx':text='\n'.join(paragraphs(z.read('word/document.xml')))
  else:
   # Relationship IDs map each slide to its own narration notes; filenames
   # alone need not have matching numeric suffixes.
   import posixpath
   relationships={r.attrib['Id']:r.attrib for r in ET.fromstring(z.read('ppt/_rels/presentation.xml.rels'))}
   slides=[]
   for node in ET.fromstring(z.read('ppt/presentation.xml')).iter():
    if node.tag.rsplit('}',1)[-1]=='sldId':
     relation=relationships[node.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
     if relation.get('TargetMode')=='External':raise ValueError('External slide is unsupported')
     name=posixpath.normpath(posixpath.join('ppt',relation['Target']))
     if not name.startswith('ppt/slides/'):raise ValueError('Invalid slide relationship')
     slides.append(name)
   pieces=[]
   import posixpath
   for i,name in enumerate(slides):
    pieces+=['Slide '+str(i+1)]+paragraphs(z.read(name))
    rel='ppt/slides/_rels/'+name.rsplit('/',1)[1]+'.rels'
    if rel in z.namelist():
     for link in ET.fromstring(z.read(rel)):
      if link.attrib.get('Type','').endswith('/notesSlide') and link.attrib.get('TargetMode')!='External':
       target=posixpath.normpath(posixpath.join('ppt/slides',link.attrib['Target']))
       if target.startswith('ppt/notesSlides/') and target in z.namelist():pieces+=['Notes:']+paragraphs(z.read(target))
   text='\n'.join(pieces)
if len(text)>LIMIT:raise ValueError('Document text exceeds supported limit')
print(json.dumps({'text':text}))
