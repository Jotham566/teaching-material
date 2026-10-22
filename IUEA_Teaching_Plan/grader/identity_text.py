"""Private identity evidence, kept separate from redacted grading text."""
import hashlib
import json
import re
import zipfile
from pathlib import Path


def registrations(text):
    from reconcile_registrations import canonical
    pattern=r"(?<![A-Za-z0-9])\d{2,4}\s*[/_]\s*(?:UG\s*[/_]\s*)?\d{1,10}\s*[/_]\s*['’]?\s*[A-Za-z]{2,12}\s*[-/=_]\s*[A-Za-z](?![A-Za-z0-9])"
    found=[]
    for match in re.finditer(pattern,text,re.I):
        raw=match.group();sid=canonical(raw)
        found.append({'registration':sid,'quote':raw})
    return found


def names(text):
    from recover_student_names import valid_name,name_key
    result=[]
    # Support Markdown tables, bold labels, NAME on its own line, and code assignments.
    lines=text.splitlines()
    label=r'(?:student(?:\s+full)?\s+name|full\s+name|student_name|full_name|name)'
    for i,line in enumerate(lines):
        clean=re.sub(r'[*#`|]',' ',line).strip()
        m=re.match(r'(?i)^'+label+r'\s*(?:[:=]\s*|\s{2,})(.+)$',clean)
        candidate=m[1].strip().strip('"\' ;') if m else ''
        quote=line
        if not candidate and re.fullmatch(label+r'\s*:?',clean,re.I) and i+1<len(lines):
            candidate=lines[i+1].strip().strip('*| ').strip('"\' ;');quote=line+'\n'+lines[i+1]
        candidate=re.split(r'\s+(?:REG(?:ISTRATION)?|STUDENT\s+ID)\b',candidate,flags=re.I)[0].strip()
        if valid_name(candidate) and candidate in quote:
            result.append({'name':candidate,'quote':quote,'method':'explicit name label'})
    return list({name_key(x['name']):x for x in result}.values())


def archive_text(path):
    """Read bounded text members in memory; never extract paths or execute code."""
    pieces=[]
    with zipfile.ZipFile(path) as archive:
        entries=[i for i in archive.infolist() if not i.is_dir() and '__MACOSX' not in i.filename]
        if len(entries)>100 or sum(i.file_size for i in entries)>20*1024*1024:
            raise ValueError('Archive exceeds identity extraction limits')
        for entry in entries:
            ext=Path(entry.filename).suffix.lower()
            if ext not in ('.ipynb','.md','.txt','.py','.sql'):continue
            data=archive.read(entry)
            text=data.decode('utf-16' if data[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8-sig')
            if ext=='.ipynb':text='\n'.join(''.join(c.get('source',[])) for c in json.loads(text).get('cells',[]))
            pieces.append(text)
    if not pieces:raise ValueError('Archive contains no supported identity text; review original archive')
    return '\n\n'.join(pieces)


def prepare(ledger,base,out,allow_documents=True):
    """Read original bytes; sandbox document extraction before stopping Docker for AI."""
    from refresh_ca import read,write,digest,ensure_docker
    cache=read(out/'identity_raw_text.json',{})
    started=False
    for row in ledger['attempts']:
        if not row.get('file_ids'):continue
        meta=read(base/'reconciled'/row['source'],{})
        for file in meta.get('files',[]):
            if file['id'] not in row['file_ids']:continue
            sha=file['sha256']
            if sha in cache and not cache[sha].get('error'):continue
            original=base/'reconciled/files'/file['export_name']
            try:
                if not original.is_file() or original.stat().st_size>20*1024*1024 or digest(original)!=sha:
                    raise ValueError('Original attachment unavailable or checksum mismatch')
                ext=original.suffix.lower()
                if ext=='.ipynb':
                    nb=json.loads(original.read_text(encoding='utf-8-sig'))
                    text='\n'.join(''.join(c.get('source',[])) for c in nb.get('cells',[]))
                elif ext in ('.md','.txt','.py','.sql'):
                    data=original.read_bytes();text=data.decode('utf-16' if data[:2] in (b'\xff\xfe',b'\xfe\xff') else 'utf-8-sig')
                elif ext=='.zip':text=archive_text(original)
                elif ext in ('.pdf','.docx','.pptx') and allow_documents:
                    if not started:ensure_docker();started=True
                    from render_submission import extract_document
                    text=extract_document(original)
                else:raise ValueError('Original format needs manual review or sandbox document extraction')
                cache[sha]={'text':text[:20000],'error':'','truncated':len(text)>20000}
            except Exception as exc:cache[sha]={'text':'','error':str(exc)[:300]}
            write(out/'identity_raw_text.json',cache)
            if len(cache)%25==0:print(f'Original identity files checked: {len(cache)}',flush=True)
    return cache
