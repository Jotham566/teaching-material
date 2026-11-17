"""Extract written evidence before loading the local AI model.

Document rendering uses the existing isolated renderer. The resulting private
text is hash-linked to the original attachment; uploaded code is never run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import artifact_grade as grading
import evidence_extract

HERE=Path(__file__).resolve().parent


def share(record):
    """Several files are read together, so give each a fair share of the combined text limit."""
    files=record['files']
    if len(files)<2:return
    each=max(2000,(evidence_extract.BUDGET-400*len(files))//len(files))
    for f in files:
        path=Path(f['path']);text=path.read_text(encoding='utf-8')
        if len(text)>each:
            content=evidence_extract.condense(text,each).encode('utf-8');path.write_bytes(content)
            f['text_sha256']=hashlib.sha256(content).hexdigest()


def prepare(source,ledger,out):
    source,out=Path(source),Path(out)
    out.mkdir(parents=True,exist_ok=True)
    previous=json.loads((out/'prepared.json').read_text()) if (out/'prepared.json').exists() else {}
    prepared={}
    for r in json.loads(Path(ledger).read_text())['current']:
        if r['assessment'] not in ('W01','W02') or r['timing_status']!='ON_TIME':continue
        record=dict(files=[],errors=[])
        rubric=json.loads((HERE/'rubrics'/f'{r["assessment"]}.json').read_text())
        record['extractor_fingerprint']=grading.evaluator_fingerprint(rubric)
        meta=json.loads((source/r['source']).read_text())
        files={f['id']:f for f in meta['files']}
        old=previous.get(r['response_id'],{})
        if (old and not old.get('errors') and old.get('extractor_fingerprint')==record['extractor_fingerprint']
                and {f['id'] for f in old.get('files',[])}==set(r['file_ids'])
                and all(f['id'] in files and f['source_sha256']==files[f['id']]['sha256']
                        and Path(f['path']).is_file()
                        and hashlib.sha256(Path(f['path']).read_bytes()).hexdigest()==f['text_sha256']
                        for f in old.get('files',[]))):
            prepared[r['response_id']]=old
            continue
        for fid in r['file_ids']:
            try:
                f=files[fid]
                original=source/'files'/f['export_name']
                # Re-uploaded data files are not written evidence.
                if original.suffix.lower()=='.csv':continue
                if hashlib.sha256(original.read_bytes()).hexdigest()!=f['sha256']:
                    raise ValueError('Original attachment checksum mismatch')
                text=evidence_extract.extract(original,r['assessment'])
                content=text.encode('utf-8')
                target=out/(hashlib.sha256((r['response_id']+'|'+fid).encode()).hexdigest()+'.md')
                target.write_bytes(content)
                record['files'].append(dict(id=fid,source_sha256=f['sha256'],path=str(target.resolve()),
                                            text_sha256=hashlib.sha256(content).hexdigest()))
            except Exception as exc:
                record['errors'].append(dict(id=fid,error=str(exc)[:400]))
        share(record)
        prepared[r['response_id']]=record
        (out/'prepared.json').write_text(json.dumps(prepared,indent=2))
    (out/'prepared.json').write_text(json.dumps(prepared,indent=2))
    print('Written packets prepared:',len(prepared),
          '; packets with extraction problems:',sum(bool(r['errors']) for r in prepared.values()))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','ledger','out'):p.add_argument('--'+name,required=True)
    a=p.parse_args()
    prepare(a.source,a.ledger,a.out)
