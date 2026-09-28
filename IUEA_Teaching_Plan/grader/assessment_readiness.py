"""Report current calibration coverage without opening forms or changing marks."""
import argparse,csv,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]

def report(evidence):
 from artifact_grade import local_model_identity,validate_calibration
 from calibration_record import model_for_report,profile_for_report
 from reasoned_artifact_grade import load_backend
 evidence=Path(evidence);identities={};rows=[]
 reports=[p for p in evidence.glob('*.json') if p.with_suffix(p.suffix+'.complete.json').is_file()]
 records=json.loads((ROOT/'data/assessments.json').read_text())
 for aid in dict.fromkeys(r['id'] for r in records):
  row=dict(assessment=aid,final_grading='HELD',calibration=None,whole_packet=None)
  if aid=='W01':row['final_grading']='PRESERVE_EXISTING';row['note']='Do not regrade already taught Week 1.'
  elif aid in ('W03','W04','W05','S05'):
   row['final_grading']='DETERMINISTIC';row['note']='No reasoning model required. Submission window and live release gate still apply.'
  else:
   path=HERE/'rubrics'/('W02.json' if aid=='W02' else 'hybrid/'+aid+'.json')
   if path.exists():
    rubric=json.loads(path.read_text());matches=[]
    for candidate in reports:
     try:
      result=json.loads(candidate.read_text())
      if not isinstance(result,list) or not result or result[0].get('result',{}).get('rubric_id') not in (None,rubric['id']):continue
      model=model_for_report(candidate);profile=profile_for_report(candidate)
      if model not in identities:identities[model]=local_model_identity(model)
      validator=load_backend().validate_calibration if profile=='reasoned' else validate_calibration
      validator(candidate,rubric,identities[model],model)
      matches.append((candidate,model,profile))
     except (ValueError,KeyError,TypeError,OSError):continue
    if matches:
     candidate,model,profile=max(matches,key=lambda x:x[0].stat().st_mtime_ns)
     row.update(final_grading='CALIBRATED',calibration=str(candidate.resolve()),model=model,profile=profile)
     row['note']='Known-answer calibration passes; this is not permission to open the form.'
    else:row['note']='No complete passing calibration matches the current rubric, evaluator and installed local model.'
   else:row['note']='The complete assessment evidence route is not yet validated.'
   packets=([evidence/'qa_current_v10/results.csv'] if aid=='W02' else [evidence/'qa_W09_current_v2/results.csv'] if aid=='W09' else list(evidence.glob(f'qa_{aid}_complete_v*/results.csv')))
   packets=[p for p in packets if p.exists()]
   if packets:
    packet=max(packets,key=lambda p:p.stat().st_mtime_ns)
    with packet.open() as f:results=list(csv.DictReader(f))
    passed=bool(results) and all(r['status']=='AUTO_SCORED' and float(r['score'])==float(r['maximum']) for r in results)
    row['latest_packet_result']=str(packet.resolve())
    row['latest_packet_passed']=passed
    if passed:row['whole_packet']=str(packet.resolve())
    elif row['final_grading']=='CALIBRATED':
     row['final_grading']='CALIBRATED_PACKET_FAILED'
     row['note']='Text calibration passes, but the latest complete-packet pilot has unresolved or incorrect results. Keep release held.'
   if aid=='S13':row['note']='40/100 numerical marks have isolated checks; the remaining 60 and complete-packet calibration are required.'
   if aid=='S15':row['note']='20/100 reported-value marks have checks; live model, chart and narrative evidence remain unvalidated.'
  rows.append(row)
 return rows

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence',required=True);p.add_argument('--out',required=True);a=p.parse_args()
 rows=report(a.evidence);out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(rows,indent=2)+'\n')
 for row in rows:print(row['assessment'],row['final_grading'],'packet tested' if row['whole_packet'] else '')
if __name__=='__main__':main()
