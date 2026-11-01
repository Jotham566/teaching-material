"""Grade A1/A2 written evidence locally, only with a passing current calibration.

Run after the notebook batch and after freeing memory used by Docker.
Every result is keyed by receipt; identity conflicts remain withheld by the ledger.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
import artifact_grade
import attachment_expand
from calibration_record import model_for_report, profile_for_report
from hybrid_result import combine
from local_ai_resources import ensure_docker_stopped

HERE=Path(__file__).resolve().parent
# Fixed so file-selection fixes do not invalidate marks already graded by the unchanged scoring path.
WRAPPER_SIGNATURE='3d8916dee5b01924d89fe1426d5427574c52ee97ca9887f66c3ac0038bdec7ae'


REVIEW_NOTES={
 'NO_NOTEBOOK_CODE_ZERO':'No usable notebook was submitted, so the code component is 0/14; the written part was marked from the uploaded report.',
 'NO_README_NOTEBOOK_TEXT_USED':'No README was uploaded; the written part was marked from the notebook\'s own explanation cells.'
}

# Files that can never be the written report or README the instructions ask for.
WRONG_TYPES={'.zip','.rar','.7z','.tar','.gz','.py','.csv','.xlsx','.xls','.json'}
GUIDES=HERE.parent/'student_guides'

def instructions_for(cohort,assessment):
    """The student-facing brief, so the marker judges work against what was actually asked."""
    path=GUIDES/cohort/(assessment+'.md')
    if not path.is_file():return None
    keep=[];
    for line in path.read_text().splitlines():
        if line.startswith('## Help only'):break
        if line.startswith(('**Deadline','**Submission link')):continue
        keep.append(line)
    text='\n'.join(keep).strip()
    return ('Assignment instructions given to students. Award marks only for work that follows them; '
            'work in a format the instructions do not allow, or that is missing a required part, earns zero for the affected criteria.\n'+text)[:3000]

QUOTE_ERROR='verifiable quoted evidence'

def snap(quote,text):
    """Return the exact passage of text that the model's near-verbatim quote refers to, or None."""
    from difflib import SequenceMatcher
    if not quote or len(quote)<25:return None
    spans=[m.span() for m in re.finditer(r'[^\n.!?]+[.!?]?',text) if m.group().strip()]
    best,top=None,0.0
    # A quote may cover one sentence or a few neighbouring ones; every candidate is a contiguous slice of text.
    for i in range(len(spans)):
        for j in range(i,min(i+3,len(spans))):
            piece=text[spans[i][0]:spans[j][1]].strip()
            ratio=SequenceMatcher(None,piece,quote,autojunk=False).ratio()
            if ratio>top:best,top=piece,ratio
    return best if top>=.85 else None

def repair_quotes(evidence,paths,assessment):
    """Fix unverifiable quotes without touching the calibrated grader: snap near-matches to the real text,
    and score a criterion 0 where no genuine supporting passage exists."""
    if QUOTE_ERROR not in str(evidence.get('error','')):return evidence
    text='\n\n'.join('Artifact %d\n%s'%(i+1,artifact_grade.extract(p,assessment)) for i,p in enumerate(sorted(map(Path,paths))))
    evaluations=json.loads(json.dumps(evidence['evaluations']));dropped=0
    for e in evaluations:
        for c in e.get('criteria',[]):
            q=c.get('evidence','')
            if c.get('awarded',0)>0 and (not q or q not in text):
                fixed=snap(q,text)
                if fixed:c['evidence']=fixed
                else:
                    c['awarded']=0;c['evidence']='';dropped+=1
                    c['feedback']=(c.get('feedback','')+' No supporting passage could be verified, so 0.')[:240]
    fixed=dict(evidence,evaluations=evaluations,status='EXCEPTION',repaired_quotes=True,dropped_unverified=dropped)
    fixed.pop('error',None)
    return fixed

def settle(evidence):
    """Differing passes are averaged, not held. Only concerns or invalid output stay unmarked."""
    passes=evidence.get('evaluations',[])
    if (evidence.get('status')=='EXCEPTION' and not evidence.get('error') and len(passes)==2
            and not any(e.get('concerns') for e in passes)):
        scores=[round(sum(c['awarded'] for c in e['criteria']),2) for e in passes]
        return dict(evidence,status='AUTO_SCORED',score=round(sum(scores)/2,2),averaged_passes=scores),scores
    return evidence,None

def explain(evidence,rubric,reason,scores):
    titles={c['id']:c['title'] for c in rubric['criteria']}
    parts=[REVIEW_NOTES[reason]] if reason in REVIEW_NOTES else []
    if evidence.get('repaired_quotes'):
        parts.append('Quotes the AI could not verify were corrected to the student\'s exact text'+(f'; {evidence["dropped_unverified"]} criterion award(s) had no verifiable support and were scored 0.' if evidence.get('dropped_unverified') else '.'))
    if scores:parts.append(f'The two AI passes scored {scores[0]} and {scores[1]}; the mark is their average.')
    first=(evidence.get('evaluations') or [{}])[0]
    detail='; '.join(f"{titles.get(c['id'],c['id'])} {c['awarded']}: {c.get('feedback','')}".strip() for c in first.get('criteria',[]))
    if detail:parts.append('Pass 1 - '+detail)
    return ' '.join(parts)[:1500]

def settle_held(old):
    """Turn a result held only because the two AI passes differed into a marked one, without re-running the model."""
    if old.get('status')!='WRITTEN_REVIEW' or not old.get('evidence'):return old
    rubric=json.loads((HERE/'rubrics'/f"{old['assessment']}.json").read_text())
    evidence,scores=settle(old['evidence'])
    if evidence.get('status')!='AUTO_SCORED':return old
    if old['assessment']=='W02':
        if old.get('code_score') is None or not old.get('code_maximum'):return old
        if scores or 'deterministic' not in evidence:
            evidence=combine(evidence,rubric,dict(status='OK',notebook_total=old['code_score'],max_total=old['code_maximum']),14,20)
    if evidence.get('status')!='AUTO_SCORED' or evidence.get('score') is None:return old
    return dict(old,status='GRADED',score=evidence['score'],evidence=evidence,
                grading_note=explain(evidence,rubric,old.get('review_reason'),scores))

def run(source, ledger, coding, calibration, assessment, out, prepared, on_progress=None):
    source, out = Path(source), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rubric=json.loads((HERE/'rubrics'/f'{assessment}.json').read_text())
    model=model_for_report(calibration)
    backend=artifact_grade
    if profile_for_report(calibration)=='reasoned':
        from reasoned_artifact_grade import load_backend
        backend=load_backend()
    identity=backend.local_model_identity(model)
    calibration_hash=backend.validate_calibration(calibration,rubric,identity,model)
    code={r['response_id']:r for r in json.loads(Path(coding).read_text())}
    prepared=json.loads(Path(prepared).read_text())
    results=[];consecutive_errors=0
    for receipt in json.loads(Path(ledger).read_text())['current']:
        if receipt['assessment']!=assessment:continue
        result={k:receipt[k] for k in ('cohort','assessment','student_id','response_id')}
        result.update(score=None,status='WRITTEN_PENDING')
        if receipt['timing_status']!='ON_TIME' or receipt['status'] in ('IDENTITY_MISSING','EQUAL_TIME_CONFLICT'):
            result['status']=receipt['status'];results.append(result);continue
        manifest=json.loads((source/receipt['source']).read_text())
        files={r['id']:r for r in manifest['files']}
        if any(fid not in files for fid in receipt['file_ids']):
            result['status']='DOWNLOAD_MISSING';results.append(result);continue
        paths=[source/'files'/files[fid]['export_name'] for fid in receipt['file_ids']]
        if not paths or any(not p.is_file() for p in paths):
            result['status']='DOWNLOAD_MISSING';results.append(result);continue
        for fid,path in zip(receipt['file_ids'],paths):
            if hashlib.sha256(path.read_bytes()).hexdigest()!=files[fid]['sha256']:
                raise ValueError('Written attachment checksum mismatch')
        result['source_hashes']={fid:files[fid]['sha256'] for fid in receipt['file_ids']}
        deterministic=None;needs_review=None
        # ZIPs and GitHub links are opened (read only); their notebook/README counts as the submission.
        inside=[m for p in paths if p.suffix.lower() in ('.zip','.html','.htm') for m in attachment_expand.expanded(p,out/'expanded')]
        direct_notebooks=any(p.suffix.lower()=='.ipynb' for p in paths)
        if inside and not direct_notebooks:
            inside_notebooks=list({m['sha256']:m for m in inside if m['original_name'].lower().endswith('.ipynb')}.values())
        else:inside_notebooks=[]
        if not inside and all(p.suffix.lower() in WRONG_TYPES for p in paths):
            # Only archives, data or script files: the required report/notebook and README were not submitted.
            uploaded=', '.join(sorted({files[fid].get('original_name',fid) for fid in receipt['file_ids']}))[:300]
            wanted='a DOCX/PDF report (or PPTX with notes)' if assessment=='W01' else 'a notebook (.ipynb) and a README'
            result.update(status='GRADED',score=0,
                          grading_note=f'Instructions require {wanted}; none was submitted, so the assignment scores 0/20. Uploaded: {uploaded}')
            if assessment=='W02':result.update(code_score=0,code_maximum=14)
            results.append(result);continue
        if assessment=='W02':
            prior=code.get(receipt['response_id'],{})
            # Duplicate uploads of one file count once.
            unique={hashlib.sha256(p.read_bytes()).hexdigest():p for p in paths}.values()
            from grade_ca_batch import HELPER_NOTEBOOK
            # Practice notebooks uploaded alongside the submission are not a second submission.
            names={hashlib.sha256(p.read_bytes()).hexdigest():files[fid]['original_name'] for fid,p in zip(receipt['file_ids'],paths)}
            notebooks=sum(p.suffix.lower()=='.ipynb' and not HELPER_NOTEBOOK.search(re.sub(r'\.ipynb.*$','',names[h],flags=re.I).strip())
                          for h,p in {hashlib.sha256(p.read_bytes()).hexdigest():p for p in paths}.items())
            notebooks+=sum(not HELPER_NOTEBOOK.search(re.sub(r'\.ipynb.*$','',m['original_name'],flags=re.I).strip()) for m in inside_notebooks)
            usable_missing=(notebooks==0 and prior.get('status')=='NOTEBOOK_MISSING_OR_AMBIGUOUS') or prior.get('status') in ('EMPTY_NOTEBOOK','INVALID_NOTEBOOK')
            if usable_missing:
                # Written work without a notebook earns no code marks and is always reviewed.
                prior=dict(prior,status='PARTIAL_CODE_ONLY',code_score=0,code_maximum=14)
                needs_review='NO_NOTEBOOK_CODE_ZERO'
            if prior.get('status')!='PARTIAL_CODE_ONLY':
                result['status']=prior.get('status','CODING_PENDING');results.append(result);continue
            if prior.get('source_hashes')!=result['source_hashes']:
                result['status']='CODING_STALE';results.append(result);continue
            result.update(code_score=prior['code_score'],code_maximum=prior['code_maximum'])
            if notebooks>1:
                result['status']='README_OR_NOTEBOOK_MISSING';results.append(result);continue
            if not needs_review and notebooks==1 and not any(p.suffix.lower() in ('.md','.txt') for p in unique) and not any(m['original_name'].lower().endswith(('.md','.txt')) for m in inside):
                # The written part is then read from the notebook's own text cells; reviewer confirms.
                needs_review='NO_README_NOTEBOOK_TEXT_USED'
            deterministic=dict(status='OK',notebook_total=prior['code_score'],max_total=prior['code_maximum'])
        packet=prepared.get(receipt['response_id'],{})
        evidence_ids={fid for fid,p in zip(receipt['file_ids'],paths) if p.suffix.lower()!='.csv'}
        readable={t['id'] for t in packet.get('files',[])}
        # One unreadable extra file must not hold work that has a readable report or notebook beside it.
        unread=sorted(evidence_ids-readable)
        if not evidence_ids or not readable or not readable<=evidence_ids or (unread and not packet.get('errors')):
            result['status']='TEXT_EXTRACTION_PENDING';results.append(result);continue
        if unread:evidence_ids=readable
        if packet.get('extractor_fingerprint')!=artifact_grade.evaluator_fingerprint(rubric):
            raise ValueError('Prepared text uses a different extractor; prepare it again')
        evidence_paths=[];seen_sources=set()
        for text in packet['files']:
            path=Path(text['path'])
            if text['source_sha256'] in seen_sources:continue
            seen_sources.add(text['source_sha256'])
            if text['source_sha256']!=result['source_hashes'].get(text['id']):
                raise ValueError('Prepared text does not match the current source')
            if hashlib.sha256(path.read_bytes()).hexdigest()!=text['text_sha256']:
                raise ValueError('Prepared text checksum mismatch')
            evidence_paths.append(path)
        signature=hashlib.sha256(json.dumps(dict(
            packet=backend.packet_hash(paths),calibration=calibration_hash,deterministic=deterministic,
            extracted_packet=backend.packet_hash(evidence_paths),
            identity=identity,student_id=receipt['student_id'],cohort=receipt['cohort'],
            combiner=hashlib.sha256((HERE/'hybrid_result.py').read_bytes()).hexdigest(),
            wrapper=WRAPPER_SIGNATURE
        ),sort_keys=True).encode()).hexdigest()
        target=out/(hashlib.sha256(receipt['response_id'].encode()).hexdigest()+'.json')
        old=json.loads(target.read_text()) if target.exists() else {}
        if old.get('signature')==signature and old.get('status')=='GRADED':
            results.append(old);continue
        if old.get('signature')==signature and old.get('status')=='WRITTEN_REVIEW' and old.get('evidence'):
            # Earlier runs held these for review; settle them from the saved AI passes without re-running the model.
            evidence,scores=settle(repair_quotes(old['evidence'],evidence_paths,assessment))
            if deterministic and evidence.get('status')=='AUTO_SCORED' and (scores or 'deterministic' not in evidence):
                evidence=combine(evidence,rubric,deterministic,14,20)
            if evidence.get('status')=='AUTO_SCORED' and evidence.get('score') is not None:
                old.update(status='GRADED',score=evidence['score'],evidence=evidence,
                           grading_note=explain(evidence,rubric,old.get('review_reason'),scores))
            else:old['score']=None
            target.write_text(json.dumps(old,indent=2));results.append(old);continue
        # Resource failures stop the batch, never become a student's grading error.
        ensure_docker_stopped()
        try:
            evidence,scores=settle(repair_quotes(backend.grade_packet(evidence_paths,dict(rubric,assignment_instructions=instructions_for(receipt['cohort'],assessment)),'ollama',model),evidence_paths,assessment))
            if deterministic:evidence=combine(evidence,rubric,deterministic,14,20)
            result.update(status='GRADED' if evidence['status']=='AUTO_SCORED' else 'WRITTEN_REVIEW',
                          review_reason=needs_review,
                          grading_note=(explain(evidence,rubric,needs_review,scores)+(f' {len(unread)} other uploaded file(s) could not be read; marked from the readable files.' if unread else ''))[:1500],
                          score=evidence['score'],evidence=evidence,signature=signature)
            # A review hold must not carry a mark; the suggestion stays in the evidence.
            if result['status']!='GRADED':result['score']=None
        except Exception as exc:
            result.update(status='WRITTEN_ERROR',error=str(exc)[:400])
        target.write_text(json.dumps(result,indent=2))
        results.append(result)
        (out/'results.json').write_text(json.dumps(results,indent=2))
        print(receipt['cohort'],assessment,result['status'],flush=True)
        consecutive_errors=consecutive_errors+1 if result['status']=='WRITTEN_ERROR' else 0
        if on_progress:on_progress(len(results),False)
        if consecutive_errors>=3:raise RuntimeError('Three consecutive local grading errors; stopped with unfinished marks pending.')
    (out/'results.json').write_text(json.dumps(results,indent=2))
    if on_progress:on_progress(len(results),True)
    return results


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source','ledger','coding','calibration','out','prepared'):parser.add_argument('--'+name,required=True)
    parser.add_argument('--assessment',choices=['W01','W02'],required=True)
    a=parser.parse_args()
    run(a.source,a.ledger,a.coding,a.calibration,a.assessment,a.out,a.prepared)
