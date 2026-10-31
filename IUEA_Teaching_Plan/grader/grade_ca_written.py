"""Grade A1/A2 written evidence locally, only with a passing current calibration.

Run after the notebook batch and after freeing memory used by Docker.
Every result is keyed by receipt; identity conflicts remain withheld by the ledger.
"""
import argparse
import hashlib
import json
from pathlib import Path
import artifact_grade
from calibration_record import model_for_report, profile_for_report
from hybrid_result import combine
from local_ai_resources import ensure_docker_stopped

HERE=Path(__file__).resolve().parent
# Fixed so file-selection fixes do not invalidate marks already graded by the unchanged scoring path.
WRAPPER_SIGNATURE='3d8916dee5b01924d89fe1426d5427574c52ee97ca9887f66c3ac0038bdec7ae'


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
        if assessment=='W02':
            prior=code.get(receipt['response_id'],{})
            # Duplicate uploads of one file count once.
            unique={hashlib.sha256(p.read_bytes()).hexdigest():p for p in paths}.values()
            notebooks=sum(p.suffix.lower()=='.ipynb' for p in unique)
            if notebooks==0 and prior.get('status')=='NOTEBOOK_MISSING_OR_AMBIGUOUS':
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
            if notebooks==1 and not any(p.suffix.lower() in ('.md','.txt') for p in unique):
                # The written part is then read from the notebook's own text cells; reviewer confirms.
                needs_review='NO_README_NOTEBOOK_TEXT_USED'
            deterministic=dict(status='OK',notebook_total=prior['code_score'],max_total=prior['code_maximum'])
        packet=prepared.get(receipt['response_id'],{})
        if (packet.get('errors') or len(packet.get('files',[]))!=len(paths)
                or {t['id'] for t in packet.get('files',[])}!=set(receipt['file_ids'])):
            result['status']='TEXT_EXTRACTION_PENDING';results.append(result);continue
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
        if old.get('signature')==signature and old.get('status') in ('GRADED','WRITTEN_REVIEW'):
            if old['status']!='GRADED':old['score']=None
            results.append(old);continue
        # Resource failures stop the batch, never become a student's grading error.
        ensure_docker_stopped()
        try:
            evidence=backend.grade_packet(evidence_paths,rubric,'ollama',model)
            if deterministic:evidence=combine(evidence,rubric,deterministic,14,20)
            result.update(status='GRADED' if evidence['status']=='AUTO_SCORED' and not needs_review else 'WRITTEN_REVIEW',
                          review_reason=needs_review,
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
