"""Incrementally grade downloaded W02–W05 notebooks in Docker, by receipt ID.
Run only after source exports and identity/timing checks have completed.
W02 code marks remain a partial component until its calibrated text marks exist.
"""
import argparse,hashlib,json,shutil,tempfile
from pathlib import Path
import batch_grade as bg
import iuea_grader as ig
from registration import filename_id
from continuous_assessment import norm

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def fingerprint():
 h=hashlib.sha256()
 for p in sorted([HERE/'Dockerfile']+list(HERE.glob('*.py'))+[p for p in (HERE/'specs').rglob('*') if p.suffix in ('.py','.json')]):
  h.update(str(p.relative_to(HERE)).encode());h.update(p.read_bytes())
 return h.hexdigest()

def run(source,ledger,out):
 source=Path(source);out=Path(out);out.mkdir(parents=True,exist_ok=True)
 current=json.loads(Path(ledger).read_text())['current'];engine=fingerprint();results=[]
 for r in current:
  if r['assessment'] not in ('W02','W03','W04','W05'):continue
  response_hash=hashlib.sha256(r['response_id'].encode()).hexdigest()
  cache=out/(response_hash+'.json')
  result={k:r[k] for k in ('cohort','assessment','student_id','response_id')}
  result.update(score=None,status=r['status'])
  # A conflicting identity does not prevent checking the work itself.
  # The ledger retains the source score but withholds cumulative allocation.
  if r['timing_status']!='ON_TIME' or r['status'] in ('IDENTITY_MISSING','EQUAL_TIME_CONFLICT'):
   results.append(result);continue
  meta=json.loads((source/r['source']).read_text());files={f['id']:f for f in meta['files']}
  if meta.get('source_kind')=='audit_only':
   result['status']='DOWNLOAD_PENDING';results.append(result);continue
  if any(fid not in files for fid in r['file_ids']):
   result['status']='DOWNLOAD_MISSING';results.append(result);continue
  result['source_hashes']={fid:files[fid]['sha256'] for fid in r['file_ids']}
  notebooks=[files[fid] for fid in r['file_ids'] if fid in files and files[fid]['export_name'].endswith('.ipynb')]
  if len(notebooks)!=1:result['status']='NOTEBOOK_MISSING_OR_AMBIGUOUS';results.append(result);continue
  info=notebooks[0];file=source/'files'/info['export_name']
  if not file.is_file():result['status']='DOWNLOAD_MISSING';results.append(result);continue
  digest=hashlib.sha256(file.read_bytes()).hexdigest()
  if digest!=info['sha256']:raise ValueError('Downloaded notebook hash mismatch')
  if not file.stat().st_size:
   result['status']='EMPTY_NOTEBOOK';results.append(result);continue
  try:
   notebook=json.loads(file.read_text(encoding='utf-8'))
   if not isinstance(notebook,dict) or not isinstance(notebook.get('cells'),list):raise ValueError('Missing cells')
  except (UnicodeError,ValueError):
   result['status']='INVALID_NOTEBOOK';results.append(result);continue
  assignment=r['assessment'];cohort=r['cohort']
  data_dir=ROOT/('IUEA_Teaching_Plan/setup/'+cohort if assignment=='W02' else 'IUEA_Teaching_Plan/practicals/'+assignment+'/'+cohort)
  data_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(data_dir.glob('*.csv'))}
  signature=hashlib.sha256(json.dumps([digest,engine,cohort,assignment,r['student_id'],data_hashes],sort_keys=True).encode()).hexdigest()
  if cache.exists():
   old=json.loads(cache.read_text())
   if old.get('signature')==signature and old['status'] in ('GRADED','PARTIAL_CODE_ONLY'):
    results.append(old);continue
  spec=ig.find_spec_file(assignment,None);hidden=ig.find_hidden_spec_file(assignment,None)
  if not spec or not hidden:raise ValueError('Both visible and private authoritative checks are required')
  with tempfile.TemporaryDirectory(prefix='ca_receipt_') as tmp:
   target=Path(tmp)/(filename_id(r['student_id'])+'_'+assignment+'.ipynb');shutil.copy2(file,target)
   record=bg.grade_one(str(target),spec,hidden,assignment,cohort,str(data_dir) if data_dir.exists() else None,30,180,None)
  if record['status']=='IDENTITY_MISMATCH' and norm(record.get('declared_sid'))==r['student_id']:
   record['identity_note']='Notebook identity matches the receipt after whitespace/filename-separator normalization; original declared_sid retained.'
   record['status']='ERRORS' if record.get('cell_errors') else 'OK'
  qs=record.get('questions') or {};maximum=sum(q.get('marks',0) for q in qs.values());score=sum(q.get('awarded',0) for q in qs.values())
  if any(q.get('err') for q in qs.values()):record['status']='GRADER_EXCEPTION'
  expected=14 if assignment=='W02' else 20
  valid=record['status'] in ('OK','ERRORS') and maximum==expected
  if record['status'] in ('OK','ERRORS') and maximum!=expected:record['status']='CHECK_MAXIMUM_MISMATCH'
  result.update(status=('PARTIAL_CODE_ONLY' if assignment=='W02' else 'GRADED') if valid else record['status'],score=score if valid and assignment!='W02' else None,code_score=score if valid else None,code_maximum=maximum,signature=signature,record=record)
  cache.write_text(json.dumps(result,indent=2)+'\n');results.append(result)
  (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  print(cohort,assignment,result['status'],flush=True)
 (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 return results
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 for name in ('source','ledger','out'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();run(a.source,a.ledger,a.out)
