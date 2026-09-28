"""Run authored known-answer cases against one local rubric; retain every result."""
import argparse,json,tempfile,time
from pathlib import Path
from artifact_grade import grade_packet

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for name in ('rubric','cases','out'):p.add_argument('--'+name,required=True)
 p.add_argument('--model',default='qwen3:4b');p.add_argument('--profile',choices=['standard','reasoned'],default='standard');args=p.parse_args()
 scorer=grade_packet
 if args.profile=='reasoned':
  from reasoned_artifact_grade import load_backend
  scorer=load_backend().grade_packet
 rubric=json.loads(Path(args.rubric).read_text());cases=json.loads(Path(args.cases).read_text());results=[]
 if len(cases)<5 or len({c['case'] for c in cases})!=len(cases):raise ValueError('At least five distinct authored cases required')
 if Path(args.out).exists():raise ValueError('Use a new evidence filename; previous calibration is retained')
 for case in cases:
  with tempfile.TemporaryDirectory() as d:
   file=Path(d)/'response.md';file.write_text(case['text']);start=time.monotonic()
   try:result=scorer([file],rubric,'ollama',args.model)
   except Exception as exc:result=dict(status='EXCEPTION',error=str(exc))
   result['evaluation_profile']=args.profile
   low,high=case['expected_range'];passed=result['status']=='AUTO_SCORED' and low<=result['score']<=high
   results.append(dict(case=case['case'],expected_range=[low,high],passed=passed,seconds=round(time.monotonic()-start,2),result=result))
   Path(args.out).write_text(json.dumps(results,indent=2));print(case['case'],'PASS' if passed else 'FAIL',result.get('score'),flush=True)
 from calibration_record import complete
 complete(args.out,[c['case'] for c in cases])
 if not all(r['passed'] for r in results):raise SystemExit(1)
if __name__=='__main__':main()
