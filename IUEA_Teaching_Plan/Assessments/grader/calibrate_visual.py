"""Run known visual defects locally; never overwrite an earlier calibration."""
import argparse,json,time
from pathlib import Path
from visual_grade import evaluate,MODEL
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--model',default=MODEL);p.add_argument('--profile',choices=['standard','atomic'],default='standard');a=p.parse_args()
if a.profile=='atomic':
 from atomic_visual_grade import evaluate
if Path(a.out).exists():raise ValueError('Use a new calibration filename')
folder=Path(__file__).parent/'calibration_cases/visual';cases=json.loads((folder/'cases.json').read_text());results=[]
for case in cases:
 start=time.monotonic()
 try:result=evaluate(folder/case['image'],a.model)
 except Exception as exc:result=dict(status='EXCEPTION',error=str(exc))
 lo,hi=case['expected_range'];passed=result['status']=='AUTO_SCORED' and lo<=result['score']<=hi
 results.append(dict(case=case['case'],expected_range=[lo,hi],passed=passed,seconds=round(time.monotonic()-start,2),result=result))
 Path(a.out).write_text(json.dumps(results,indent=2));print(case['case'],'PASS' if passed else 'FAIL',result.get('score'),flush=True)
from calibration_record import complete
complete(a.out,[c['case'] for c in cases])
if not all(r['passed'] for r in results):raise SystemExit(1)
