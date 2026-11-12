"""Incrementally grade downloaded W02–W05 notebooks in Docker, by receipt ID.
Run only after source exports and identity/timing checks have completed.
W02 code marks remain a partial component until its calibrated text marks exist.
"""
import argparse,hashlib,json,re,shutil,tempfile
from pathlib import Path
import batch_grade as bg
import iuea_grader as ig
import attachment_expand
import colab_shim
import grader_fairness
from registration import filename_id
from continuous_assessment import norm

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]

def fingerprint():
 h=hashlib.sha256()
 for p in sorted([HERE/'Dockerfile']+list(HERE.glob('*.py'))+[p for p in (HERE/'specs').rglob('*') if p.suffix in ('.py','.json')]):
  h.update(str(p.relative_to(HERE)).encode());h.update(p.read_bytes())
 return h.hexdigest()

HELPER_NOTEBOOK=re.compile(r'proof[ _-]*of[ _-]*life|hidden[ _-]*state|wrong[ _-]*(?:path|runtime)|missing[ _-]*module|^copy of ',re.I)

def pick_notebook(notebooks,assignment,student_id):
 """Choose the submission notebook when extra practice notebooks were uploaded too.
 Practice/helper notebooks are ignored; if several remain, only one whose name carries
 this assignment or the student's registration is accepted. Otherwise stay ambiguous."""
 if len(notebooks)==1:return notebooks[0]
 stem=lambda n:re.sub(r'\.ipynb.*$','',n.get('original_name',''),flags=re.I)
 main=[n for n in notebooks if not HELPER_NOTEBOOK.search(stem(n).strip())]
 if len(main)==1:return main[0]
 compact=lambda v:re.sub(r'[^A-Z0-9]','',str(v).upper())
 named=[n for n in main if assignment in compact(stem(n)) or compact(student_id) in compact(stem(n))]
 return named[0] if len(named)==1 else None

def decode_notebook(raw):
 """Return notebook JSON text; accept UTF-8 (with BOM) and BOM-marked UTF-16 exports."""
 if raw[:2] in (b'\xff\xfe',b'\xfe\xff'):return raw.decode('utf-16')
 return raw.decode('utf-8-sig')

def notebook_sources(notebook_text):
 try:cells=json.loads(notebook_text).get('cells',[])
 except ValueError:return []
 return [''.join(c.get('source','')) if isinstance(c.get('source',''),list) else c.get('source','') for c in cells if c.get('cell_type')=='code']

def docx_text(path):
 """Plain text of a .docx (paragraphs and line breaks kept). Read only."""
 import html as htmllib,zipfile
 try:x=zipfile.ZipFile(path).read('word/document.xml').decode('utf-8','replace')
 except (zipfile.BadZipFile,KeyError,OSError):return ''
 out=[]
 for t,tag,endp in re.findall(r'<w:t(?: [^>]*)?>([^<]*)</w:t>|<w:(br|tab)\b[^>]*?/?>|</w:(p)>',x):
  out.append(htmllib.unescape(t) if t else '\n' if tag=='br' or endp else '\t')
 return ''.join(out)

def converted_notebook(path,name):
 """Notebook JSON text from a Colab .py export or a .docx holding the notebook JSON or pasted
 code; None when the file cannot be converted. Nothing is executed here."""
 suffix=Path(name).suffix.lower() or Path(path).suffix.lower()
 if suffix=='.py':
  text=Path(path).read_bytes().decode('utf-8-sig','replace')
  nb=colab_shim.colab_py_to_notebook(text)
  return json.dumps(nb) if nb['cells'] else None
 if suffix=='.docx':
  text=docx_text(path).strip()
  if text.startswith('{'):
   try:
    nb=json.loads(text)
    if isinstance(nb,dict) and isinstance(nb.get('cells'),list):return json.dumps(nb)
   except ValueError:pass
  spans=colab_shim.code_spans(text)
  if spans:
   nb=colab_shim.notebook_from_cells(spans,'code pasted in a .docx')
   return json.dumps(nb)
 return None

def prepare_submission(r,files,source,cache):
 """Find the notebook to grade for one receipt (fix 5, 10 Nov 2026).
 Direct .ipynb first; else notebooks inside ZIPs/GitHub links; else a Colab .py export or a
 .docx converted to a notebook. Returns a dict with status NOTEBOOK (notebook_text, sha256,
 original_name, origin_note), NO_NOTEBOOK, AMBIGUOUS, DOWNLOAD_MISSING or CANNOT_JUDGE
 (reason_code EMPTY or UNREADABLE, with reason)."""
 source=Path(source);fids=[f for f in r['file_ids'] if f in files]
 uploaded=sorted({files[f].get('original_name',f) for f in fids})
 notebooks=[files[f] for f in fids if files[f]['export_name'].lower().endswith('.ipynb')]
 notebooks=list({n['sha256']:n for n in notebooks}.values())
 origin_note=''
 if not notebooks:
  # No direct notebook: look inside ZIPs and GitHub links submitted instead (read only, never run).
  for f in fids:
   for n in attachment_expand.expanded(source/'files'/files[f]['export_name'],cache):
    if n['original_name'].lower().endswith('.ipynb'):notebooks.append(n)
  notebooks=list({n['sha256']:n for n in notebooks}.values())
  if notebooks:origin_note='Notebook was not uploaded directly; '+notebooks[0]['original_name']+' was taken from '+notebooks[0]['origin']+' (no penalty). '
 if not notebooks:
  for f in fids:
   path=source/'files'/files[f]['export_name']
   if not path.is_file():continue
   text=converted_notebook(path,files[f].get('original_name',''))
   if text:
    return dict(status='NOTEBOOK',notebook_text=text,sha256=files[f]['sha256'],original_name=files[f].get('original_name',''),uploaded=uploaded,
                origin_note='No .ipynb was uploaded; the notebook was rebuilt from '+files[f].get('original_name','the upload')+' (no penalty). ')
 if not notebooks:
  if not uploaded:return dict(status='NO_NOTEBOOK',uploaded=uploaded)
  return dict(status='CANNOT_JUDGE',reason_code='UNREADABLE',uploaded=uploaded,
              reason='No notebook could be read from the upload ('+', '.join(uploaded)[:300]+'); cannot judge (no mark) - ask for the notebook.')
 info=pick_notebook(notebooks,r['assessment'],r['student_id'])
 if info is None:return dict(status='AMBIGUOUS',uploaded=uploaded)
 file=info['path'] if info.get('path') else source/'files'/info['export_name']
 if not Path(file).is_file():return dict(status='DOWNLOAD_MISSING',uploaded=uploaded)
 raw=Path(file).read_bytes();digest=hashlib.sha256(raw).hexdigest()
 if digest!=info['sha256']:raise ValueError('Downloaded notebook hash mismatch')
 if not raw:
  return dict(status='CANNOT_JUDGE',reason_code='EMPTY',uploaded=uploaded,
              reason='The uploaded notebook is empty (0 bytes); cannot judge (no mark) - ask for the file again. File: '+info.get('original_name',''))
 try:
  text=decode_notebook(raw);nb=json.loads(text)
  if not isinstance(nb,dict) or not isinstance(nb.get('cells'),list):raise ValueError('Missing cells')
 except (UnicodeError,ValueError):
  return dict(status='CANNOT_JUDGE',reason_code='UNREADABLE',uploaded=uploaded,
              reason='The uploaded file is not a readable notebook; cannot judge (no mark). File: '+info.get('original_name',''))
 return dict(status='NOTEBOOK',notebook_text=text,sha256=digest,original_name=info.get('original_name',''),origin_note=origin_note,uploaded=uploaded)

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
  prep=prepare_submission(r,files,source,out/'expanded')
  origin_note=prep.get('origin_note','')
  if prep['status']=='NO_NOTEBOOK' and r['assessment']!='W02' and not prep.get('uploaded'):
   # Instructions require a notebook. Nothing at all was uploaded: scored 0 with the reason recorded.
   result.update(status='GRADED',score=0,code_score=0,code_maximum=20,
                 grading_note='No notebook (.ipynb) was submitted, so the assignment scores 0/20. Uploaded: no files')
   results.append(result);continue
  if prep['status'] in ('NO_NOTEBOOK','CANNOT_JUDGE') and r['assessment']!='W02':
   # Lenient rule (10 Nov 2026): a wrong, empty or unreadable upload is 'cannot judge' (no mark), never 0.
   result.update(status='CANNOT_JUDGE',score=None,code_score=None,code_maximum=14 if r['assessment']=='W02' else 20,
                 grading_note=prep.get('reason') or ('No gradable notebook was found; cannot judge. Uploaded: '+', '.join(prep.get('uploaded',[]))[:300]))
   results.append(result);continue
  if prep['status'] in ('NO_NOTEBOOK','AMBIGUOUS'):result['status']='NOTEBOOK_MISSING_OR_AMBIGUOUS';results.append(result);continue
  if prep['status']=='DOWNLOAD_MISSING':result['status']='DOWNLOAD_MISSING';results.append(result);continue
  if prep['status']=='CANNOT_JUDGE':
   # W02 keeps its earlier statuses so its written part is still graded and reviewed (code part has no mark).
   result['status']=('EMPTY_NOTEBOOK' if prep.get('reason_code')=='EMPTY' else 'INVALID_NOTEBOOK' if prep.get('original_name') or 'not a readable notebook' in prep.get('reason','') else 'NOTEBOOK_MISSING_OR_AMBIGUOUS')
   results.append(result);continue
  notebook_text=prep['notebook_text'];digest=prep['sha256']
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
   target=Path(tmp)/(filename_id(r['student_id'])+'_'+assignment+'.ipynb');target.write_text(notebook_text,encoding='utf-8')
   record=bg.grade_one(str(target),spec,hidden,assignment,cohort,str(data_dir) if data_dir.exists() else None,30,180,None)
  if record['status']=='IDENTITY_MISMATCH' and norm(record.get('declared_sid'))==r['student_id']:
   record['identity_note']='Notebook identity matches the receipt after whitespace/filename-separator normalization; original declared_sid retained.'
   record['status']='ERRORS' if record.get('cell_errors') else 'OK'
  qs=record.get('questions') or {};maximum=sum(q.get('marks',0) for q in qs.values());score=sum(q.get('awarded',0) for q in qs.values())
  if any(q.get('err') for q in qs.values()):record['status']='GRADER_EXCEPTION'
  expected=14 if assignment=='W02' else 20
  valid=record['status'] in ('OK','ERRORS') and maximum==expected
  if record['status'] in ('OK','ERRORS') and maximum!=expected:record['status']='CHECK_MAXIMUM_MISMATCH'
  if origin_note:result['grading_note']=origin_note.strip()
  result.update(status=('PARTIAL_CODE_ONLY' if assignment=='W02' else 'GRADED') if valid else record['status'],score=score if valid and assignment!='W02' else None,code_score=score if valid else None,code_maximum=maximum,signature=signature,record=record)
  # A different notebook scoring 0 is 'cannot judge' (W03-W05; W02's written part stays gradable).
  wrong=grader_fairness.cannot_judge_reason(assignment,cohort,notebook_sources(notebook_text),score) if valid and assignment!='W02' else ''
  if wrong:
   result.update(status='CANNOT_JUDGE',score=None,code_score=None,grading_note=(origin_note+wrong).strip())
  cache.write_text(json.dumps(result,indent=2)+'\n');results.append(result)
  (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
  print(cohort,assignment,result['status'],flush=True)
 (out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
 return results
if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__)
 for name in ('source','ledger','out'):ap.add_argument('--'+name,required=True)
 a=ap.parse_args();run(a.source,a.ledger,a.out)
