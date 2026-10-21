"""Run validated local written grading and refresh the private workbook in batches."""
import argparse
import collections
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import shutil
import urllib.request
import artifact_grade
import continuous_assessment
import grade_ca_written
from calibration_record import model_for_report

ROOT=Path(__file__).resolve().parents[2]
_bundled_node=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
NODE=Path(os.environ.get('IUEA_NODE') or (str(_bundled_node) if _bundled_node.is_file() else shutil.which('node') or 'node'))


def merged_results(paths):
    merged={}
    for path in paths:
        if not Path(path).exists():continue
        for row in json.loads(Path(path).read_text()):
            old=merged.get(row['response_id'])
            if old and any(old[k]!=row[k] for k in ('cohort','assessment','student_id')):
                raise ValueError('Conflicting result identities')
            merged[row['response_id']]=row
    return list(merged.values())


def unload(model):
    request=urllib.request.Request('http://127.0.0.1:11434/api/generate',
        data=json.dumps(dict(model=model,keep_alive=0)).encode(),
        headers={'Content-Type':'application/json'},method='POST')
    with artifact_grade.LOCAL_HTTP.open(request,timeout=30) as response:response.read()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','ledger','coding','prepared','w1-calibration','w2-calibration','out'):
        p.add_argument('--'+name,required=True)
    a=p.parse_args()
    out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    source=Path(a.source).resolve()
    results_paths=[Path(a.coding),out/'W01/results.json',out/'W02/results.json']
    # Rebuild aggregates from individually validated caches on every run.
    # An earlier export may contain receipts or attachments since replaced.
    history=out/'history'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    for path in results_paths[1:]:
        if path.exists():
            history.mkdir(parents=True,exist_ok=True)
            path.replace(history/(path.parent.name+'_results.json'))
    status_path=out/'queue_status.json'
    active_model=None
    def status(state,**details):
        temp=status_path.with_suffix('.tmp')
        temp.write_text(json.dumps(dict(state=state,pid=os.getpid(),updated_at=datetime.now(timezone.utc).isoformat(),**details),indent=2))
        temp.replace(status_path)
    def workbook():
        result_file=out/'combined_results.json'
        result_file.write_text(json.dumps(merged_results(results_paths),indent=2))
        ledger=continuous_assessment.build(source,result_file,json.loads((source/'timing.json').read_text()))
        ledger_file=out.parent/'ledger.json'
        ledger_file.write_text(json.dumps(ledger,indent=2))
        temporary=out.parent/'IUEA_Continuous_Assessment.next.xlsx'
        subprocess.run([str(NODE),str(ROOT/'scripts/build_continuous_assessment.mjs'),
                        str(ledger_file),str(temporary)],check=True)
        os.replace(temporary,out.parent/'IUEA_Continuous_Assessment.xlsx')
        return dict(collections.Counter(r['status'] for r in ledger['current']))
    try:
        for assessment,calibration in [('W01',a.w1_calibration),('W02',a.w2_calibration)]:
            active_model=model_for_report(calibration)
            status('RUNNING',assessment=assessment)
            def checkpoint(count,finished):
                status('RUNNING',assessment=assessment,processed=count)
                if finished or count%20==0:
                    unload(active_model)
                    counts=workbook()
                    status('RUNNING',assessment=assessment,processed=count,current_statuses=counts)
            grade_ca_written.run(source,a.ledger,a.coding,calibration,assessment,out/assessment,a.prepared,checkpoint)
        unload(active_model)
        status('COMPLETE',current_statuses=workbook(),
               note='Queue complete. Unresolved identity, packet and written-review statuses remain pending, never zero.')
    except BaseException as exc:
        status('STOPPED',error=str(exc)[:500])
        raise
    finally:
        if active_model:
            try:unload(active_model)
            except Exception:pass


if __name__=='__main__':main()
