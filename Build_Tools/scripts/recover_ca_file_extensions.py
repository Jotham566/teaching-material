"""Recover unambiguous file extensions without changing uploaded bytes or hashes."""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path

def recover(source):
 source=Path(source);changes=[]
 for manifest in source.glob('*_manifest.json'):
  data=json.loads(manifest.read_text());changed=False
  for f in data['files']:
   original=source/'files'/f['export_name']
   if not original.is_file():continue
   content=original.read_bytes()
   if hashlib.sha256(content).hexdigest()!=f['sha256']:raise ValueError('Source checksum mismatch')
   extension=None
   if content.startswith(b'%PDF-'):extension='.pdf'
   elif content.startswith(b'PK'):
    try:
     with zipfile.ZipFile(original) as z:
      names=set(z.namelist())
      if '[Content_Types].xml' in names:
       if 'word/document.xml' in names:extension='.docx'
       elif 'ppt/presentation.xml' in names:extension='.pptx'
    except zipfile.BadZipFile:pass
   elif len(content)<20_000_000:
    try:
     value=json.loads(content.decode('utf-8-sig'))
     if isinstance(value,dict) and value.get('nbformat')==4 and isinstance(value.get('cells'),list):extension='.ipynb'
    except (UnicodeError,ValueError):pass
   if extension and original.suffix.lower()!=extension:
    target=original.with_suffix(extension);shutil.copyfile(original,target)
    f['original_export_name']=f['export_name'];f['export_name']=target.name
    f['format_recovery']='Extension identified from the file signature. Uploaded bytes and checksum unchanged.'
    changes.append(dict(manifest=manifest.name,file_id=f['id'],old=original.suffix,new=extension));changed=True
  if changed:manifest.write_text(json.dumps(data,indent=2))
 (source/'format_recoveries.json').write_text(json.dumps(changes,indent=2))
 return changes

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source');a=p.parse_args();print('Recovered extensions:',len(recover(a.source)))
